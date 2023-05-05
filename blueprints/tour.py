import json
import datetime

from flask import Blueprint, render_template, request, jsonify, current_app, session, redirect, url_for, flash
from model import *
from exts import db
import math
from translations.translator import translator

bp = Blueprint("tour", __name__, url_prefix="/tour")


@bp.route("/<page_num>")
def tourList(page_num):
    total_tours = Tour.query.count()
    pagination = Tour.query.filter_by(status="published").paginate(page=int(page_num), per_page=18, error_out=False)
    tours = pagination.items
    for single_tour in tours:
        # noinspection PyTypeChecker
        single_tour.images = json.loads(single_tour.images)['images']
        single_tour.images[0] = single_tour.images[0][single_tour.images[0].index('static'):].lstrip('static')
    tours = sorted(tours, key=lambda tour: tour.priority, reverse=True)
    logged = True if session.get("customer_id") else False
    result = request.args.get('result')
    return render_template("tour-grid.html", total_tours=total_tours, tours=tours, logged=logged, result=result)


@bp.route('/details/<tour_id>/', methods=['GET'])
def tourDetail(tour_id):
    tour = Tour.query.get(tour_id)
    tour.view_num = tour.view_num + 1
    db.session.commit()
    reviews = tour.review
    tour.included = json.loads(tour.included)['included']
    tour.included = [i for i in tour.included if i is not None]
    tour.excluded = json.loads(tour.excluded)['not_included']
    tour.excluded = [i for i in tour.excluded if i is not None]
    tour.images = json.loads(tour.images)['images']
    images = [image[image.index('static'):].lstrip('static') for image in tour.images]
    tour.itineraries = json.loads(tour.itineraries)['tour_des']
    tour.itineraries = [list(i.items())[0] for i in tour.itineraries]
    tour.start_time = tour.start_time.strftime("%Y-%m-%d")
    tour.end_time = tour.end_time.strftime("%Y-%m-%d")
    days = len(tour.itineraries)
    for review in reviews:
        review.customerID = Customer.query.get(review.customerID).nickname
        review.issueTime = review.issueTime.strftime("%Y-%m-%d %H:%M")
    tour.view_num = tour.view_num + 1
    wishlist_exists = TourOrder.query.filter_by(customerID=session.get("customer_id"),
                                                productID=tour_id, purchased=False).first()
    added = True if wishlist_exists is not None else False
    purchased = TourOrder.query.filter_by(customerID=session.get("customer_id"),
                                          productID=tour_id, purchased=True).first()
    logged = session.get("customer_id")
    purchased = True if (purchased is not None and logged is not None) else False
    logged = True if logged else False
    star_detail = json.loads(tour.star_detail)['star_detail']
    star_score = round(sum(star_detail) / tour.review_num, 1) if tour.review_num != 0 else 0
    star_score_ceil = math.floor(star_score)
    review_num = tour.review_num
    tour.review_num = 10000 if tour.review_num == 0 else tour.review_num
    lat = tour.lat
    lon = tour.lon
    return render_template("tour-detail.html", tour=tour, days=days, images=images, reviews=reviews, added=added,
                           purchased=purchased, logged=logged, star_score=star_score, star_score_ceil=star_score_ceil,
                           star_detail=star_detail, review_num=review_num, lat=lat, lon=lon)


@bp.route('/add_review', methods=['POST'])
def add_review():
    tour_id = request.form.get('productId')
    customer_id = session.get('customer_id')
    content = request.form.get('content')
    tour = Tour.query.get(tour_id)
    if tour is None:
        return jsonify({'code': 400, 'message': 'Activity not found'})
    # check if the customer has ordered the activity
    # order = ActivityOrder.query.filter_by(customerID=customer_id, productID=activity_id).first()
    # if order is None:
    #     return jsonify({'code': 400, 'message': 'No order'})
    tour.review_num = tour.review_num + 1
    star = int(request.form.get("rating"))
    star_index = star - 1
    star_detail = json.loads(tour.star_detail)["star_detail"]
    star_detail[star_index] = star_detail[star_index] + star
    tour.star_detail = json.dumps({"star_detail": star_detail})
    review = TourReview(rating=star, issueTime=datetime.datetime.now(), content=content, customerID=customer_id,
                        productID=tour_id)
    db.session.add(review)
    db.session.commit()
    return redirect(url_for('tour.tourDetail', tour_id=int(tour.id)))


@bp.route('/tour_filter', methods=['GET', 'POST'])
def tour_filter():
    tour_type = request.form.get("type1").split(",")
    to_sort = request.form.get('sort_by')
    if 'language' in session:
        if session["language"] == 'zh':
            key_word = request.form.get('key-word')
            key_word = translator(key_word, 'zh', 'en')
        else:
            key_word = request.form.get('key-word')
    else:
        key_word = ''
    if tour_type[0] == '':
        tour_type = ['Cultural tourism', 'Wildlife observation', 'Cruises', 'Grass Skyline']
    tour_price = request.form.get('tourPrice')
    tour_price = tour_price.split(',')
    min_price = int(tour_price[0])
    max_price = int(tour_price[-1])
    tour_duration = request.form.get('tourDuration').split(",")
    if tour_duration[0] == '':
        query = Tour.query.filter(Tour.category.in_(tour_type),
                                  Tour.price.between(min_price, max_price)
                                  )
    else:
        tour_duration = tour_duration[0].split('-')
        min_hour = int(tour_duration[0])
        max_hour = int(tour_duration[-1])
        query = Tour.query.filter(Tour.category.in_(tour_type),
                                  Tour.price.between(min_price, max_price),
                                  Tour.duration.between(min_hour, max_hour)
                                  )
    page = int(request.form.get('page'))
    pagination = query.paginate(page=page, per_page=18)
    tours = pagination.items
    for tour_i in tours:
        tour_i.contact_email = url_for('tour.tourDetail', tour_id=tour_i.id)
        tour_i.images = json.loads(tour_i.images)['images']
        tour_i.images[0] = "../" + tour_i.images[0][tour_i.images[0].index('static'):].replace('\\', '/')
    if to_sort == '1':
        tours = sorted(tours, key=lambda tour: tour.priority, reverse=True)

    if to_sort == '2':
        tours = sorted(tours, key=lambda tour: tour.view_num, reverse=True)

    if to_sort == '3':
        tours = sorted(tours, key=lambda tour: tour.price, reverse=False)

    if to_sort == '4':
        tours = sorted(tours, key=lambda tour: tour.price, reverse=True)

    tours = [tour.to_dict() for tour in tours]
    return jsonify({"tours": tours, "page": 1, "keyword": key_word})


@bp.route("/order-confirm", methods=['POST'])
def order_confirm():
    customer_id = session.get('customer_id')
    if customer_id:
        tour_id = request.form.get("tour_id")
        to_confirmed = Tour.query.get(tour_id)
        order_date = request.form.get("journey-date")
        customer = Customer.query.get(customer_id)
        return render_template("tour-booking-confirm.html", tour=to_confirmed, customer=customer,
                               order_date=order_date, logged=True)
    else:
        url = request.referrer
        return render_template("SignInUp.html", url=url)


@bp.route("/order-success")
def order_success():
    customer = Customer.query.get(session.get("customer_id"))
    cost = float(request.args.get("cost"))
    if customer.wallet >= cost:
        tour_order = TourOrder()
        tour_order.customerID = session.get('customer_id')
        tour_order.purchased = True
        tour_order.startTime = datetime.datetime.now()
        end_date = request.args.get("date")
        try:
            date_format = "%Y/%m/%d"
            datetime_obj = datetime.datetime.strptime(end_date, date_format)
        except ValueError:
            date_format = "%m/%d/%Y"
            datetime_obj = datetime.datetime.strptime(end_date, date_format)
        tour_order.endTime = datetime_obj
        tour_order.productID = request.args.get("tour_id")
        tour_order.cost = cost
        customer.wallet = customer.wallet - cost
        db.session.add(tour_order)
        db.session.commit()
        return render_template("booking-success.html", name=request.args.get("name"))
    else:
        flash("Insufficient balance in your wallet, please top up first")
        return redirect(url_for('customer.profile', page='/wallet'))


@bp.route("/add_wishlist/<tour_id>")
def add_wishlist(tour_id):
    aimed_tour = Tour.query.get(tour_id)
    tour_order = TourOrder()
    tour_order.cost = aimed_tour.price
    tour_order.startTime = datetime.datetime.now()
    tour_order.purchased = False
    tour_order.customerID = session.get("customer_id")
    tour_order.productID = tour_id
    db.session.add(tour_order)
    db.session.commit()
    return redirect(url_for('customer.profile', page="/wishlist"))


@bp.route("/remove_wishlist/<tour_id>")
def remove_wishlist(tour_id):
    tour_order = TourOrder.query.filter_by(customerID=session.get("customer_id"), productID=tour_id,
                                           purchased=False).first()
    db.session.delete(tour_order)
    db.session.commit()
    return redirect(url_for('customer.profile', page="/wishlist"))
