import json
from datetime import datetime

from flask import Blueprint, render_template, request, jsonify, current_app, session, redirect, url_for
from model import *
from exts import db

bp = Blueprint("tour", __name__, url_prefix="/tour")


@bp.route("/<page_num>")
def tourList(page_num):
    total_tours = Tour.query.count()
    pagination = Tour.query.paginate(page=int(page_num), per_page=9, error_out=False)
    tours = pagination.items
    for single_tour in tours:
        # noinspection PyTypeChecker
        single_tour.images = json.loads(single_tour.images)['images']
        single_tour.images[0] = single_tour.images[0][single_tour.images[0].index('static'):].lstrip('static')
    return render_template("tour-grid.html", total_tours=total_tours, tours=tours)


@bp.route('/details/<tour_id>/', methods=['GET'])
def tourDetail(tour_id):
    tour = Tour.query.get(tour_id)
    reviews = tour.review
    if tour is None:
        return jsonify({'code': 400, 'message': "no activity found"})
    tour.included = json.loads(tour.included)['included']
    tour.included = [i for i in tour.included if i is not None]
    tour.excluded = json.loads(tour.excluded)['not_included']
    tour.excluded = [i for i in tour.excluded if i is not None]
    tour.images = json.loads(tour.images)['images']
    images = [image[image.index('static'):].lstrip('static') for image in tour.images]
    tour.itineraries = json.loads(tour.itineraries)['tour_des']
    tour.itineraries = [list(i.items())[0] for i in tour.itineraries]
    tour.start_time = tour.start_time.strftime("%Y-%m-%d")
    tour.end_time = tour.end_time.strftime("%Y-%m-%d %H:%M")
    days = len(tour.itineraries)
    for review in reviews:
        review.customerID = Customer.query.get(review.customerID).nickname
        review.issueTime = review.issueTime.strftime("%Y-%m-%d %H:%M")
    tour.review_num = tour.review_num + 1
    wishlist_exists = TourOrder.query.filter_by(customerID=session.get("customer_id"),
                                                productID=tour_id, purchased=False).first()
    added = True if wishlist_exists is not None else False
    purchased = TourOrder.query.filter_by(customerID=session.get("customer_id"),
                                          productID=tour_id, purchased=True)
    tour.review_num = tour.review_num + 1
    db.session.commit()
    return render_template("tour-detail.html", tour=tour, days=days, images=images, reviews=reviews, added=added,
                           purchased=purchased)


@bp.route('/add_review', methods=['POST'])
def add_review():
    tour_id = request.form.get('productId')
    customer_id = session.get('customer_id')
    rating = int(request.form.get('rating'))
    content = request.form.get('content')
    # check if all the data have been entered
    if not customer_id or not rating or not content:
        return jsonify({'code': 400, 'message': 'Invalid data'})
    # check if activity exist
    tour = Tour.query.get(tour_id)
    if tour is None:
        return jsonify({'code': 400, 'message': 'Activity not found'})
    # check if the customer has ordered the activity
    # order = ActivityOrder.query.filter_by(customerID=customer_id, productID=activity_id).first()
    # if order is None:
    #     return jsonify({'code': 400, 'message': 'No order'})
    review = TourReview(rating=rating, issueTime=datetime.now(), content=content, customerID=customer_id,
                        productID=tour_id)
    tour.review_num = tour.review_num + 1
    db.session.add(review)
    db.session.commit()
    return redirect(url_for('tour.tourDetail', tour_id=int(tour.id)))


@bp.route('/tour_filter', methods=['GET', 'POST'])
def tour_filter():
    tour_type = request.form.get("type1").split(",")
    to_sort = request.form.get('sort_by')
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
    pagination = query.paginate(page=page, per_page=9)
    tours = pagination.items
    for tour_i in tours:
        tour_i.contact_email = url_for('tour.tourDetail', activity_id=tour_i.id)
        tour_i.images = json.loads(tour_i.images)['images']
        tour_i.images[0] = "../" + tour_i.images[0][tour_i.images[0].index('static'):].replace('\\', '/')

    if to_sort == '2':
        tours = sorted(tours, key=lambda tour: tour.view_num, reverse=False)

    if to_sort == '3':
        tours = sorted(tours, key=lambda tour: tour.price, reverse=False)

    if to_sort == '4':
        tours = sorted(tours, key=lambda tour: tour.price, reverse=True)

    tours = [tour.to_dict() for tour in tours]
    return jsonify({"tours": tours, "page": 1})
