import json
import math

from flask import Blueprint, session, render_template, request, url_for, redirect, jsonify, flash
from model import Flight, FlightOrder, FlightReview, Customer, Activity, ActivityOrder
import datetime
from exts import db
from datetime import time
from sqlalchemy import or_
from translations.translator import translator
from datetime import date, timedelta

bp = Blueprint("flight", __name__, url_prefix="/flight")


@bp.route('/<page_num>', methods=['POST', 'GET'])
def flightList(page_num):
    logged = False if session.get('customer_id') is None else True
    total_flights = Flight.query.count()
    pagination = Flight.query.filter_by(status="published").paginate(page=int(page_num), per_page=18, error_out=False)
    flights = pagination.items
    for flight in flights:
        # noinspection PyTypeChecker
        flight.images = json.loads(flight.images)['images']
        flight.images[0] = flight.images[0][flight.images[0].index('static'):].lstrip('static')
    flights = sorted(flights, key=lambda i: i.priority, reverse=True)
    return render_template("flight-grid.html", total_flights=total_flights, flights=flights, page_num=page_num,
                           logged=logged)


@bp.route('/details/<flight_id>')
def flightDetail(flight_id):
    flight = Flight.query.get(flight_id)
    flight.view_num += 1
    db.session.commit()
    logged = False if session.get('customer_id') is None else True
    flight.images = json.loads(flight.images)['images']
    images = [image[image.index('static'):].lstrip('static') for image in flight.images]
    wifi = True if 'WiFi' in flight.inflight_features else False
    air_condition = True if 'Air Conditioning' in flight.inflight_features else False
    coffee = True if 'Coffee' in flight.inflight_features else False
    entertainment = True if 'Entertainment' in flight.inflight_features else False
    food = True if 'Food' in flight.inflight_features else False
    drink = True if 'Drink' in flight.inflight_features else False
    wines = True if 'Wines' in flight.inflight_features else False
    comfort = True if 'Comfort' in flight.inflight_features else False
    television = True if 'Television' in flight.inflight_features else False
    game = True if 'Games' in flight.inflight_features else False
    shopping = True if 'Shopping' in flight.inflight_features else False
    magazines = True if 'Magazines' in flight.inflight_features else False
    wishlist_exists = FlightOrder.query.filter_by(customerID=session.get("customer_id"),
                                                  productID=flight_id, purchased=False).first()
    added = True if wishlist_exists is not None else False
    purchased = FlightOrder.query.filter_by(customerID=session.get("customer_id"),
                                            productID=flight_id, purchased=True).first()
    purchased = True if (purchased is not None and logged is not None) else False
    star_detail = json.loads(flight.star_detail)['star_detail']
    star_score = round(sum(star_detail) / flight.review_num, 1) if flight.review_num != 0 else 0
    star_score_ceil = math.floor(star_score)
    review_num = flight.review_num
    flight.review_num = 10000 if flight.review_num == 0 else flight.review_num
    reviews = flight.review
    for review in reviews:
        review.customerID = Customer.query.get(review.customerID).nickname
        review.issueTime = review.issueTime.strftime("%Y-%m-%d %H:%M")
    start_date = date.today()
    end_date = start_date + timedelta(days=5 * 30)
    week_days = []
    while start_date <= end_date:
        if start_date.weekday() == int(flight.week_day) - 1:
            week_days.append(start_date.strftime("%Y-%m-%d") + ',')
        start_date += timedelta(days=1)
    return render_template("flight-detail.html", logged=logged, flight=flight, images=images, wifi=wifi,
                           air_condition=air_condition, coffee=coffee
                           , entertainment=entertainment, food=food, drink=drink, wines=wines, comfort=comfort,
                           television=television, shopping=shopping, magazines=magazines, game=game,
                           star_score=star_score, star_score_ceil=star_score_ceil,
                           day_of_week=''.join(week_days), added=added, purchased=purchased, star_detail=star_detail,
                           review_num=review_num, reviews=reviews)


@bp.route("/order-confirm", methods=['POST'])
def order_confirm():
    customer_id = session.get('customer_id')
    if customer_id:
        flight_id = request.form.get("flight_id")
        to_confirmed = Flight.query.get(flight_id)
        order_date = datetime.datetime.strptime(request.form.get("journey-date"), '%m/%d/%Y').strftime(
            '%Y/%m/%d') + ' ' + to_confirmed.takeoff_time.strftime('%H:%M')
        customer = Customer.query.get(customer_id)
        arrive_time = datetime.datetime.strptime(request.form.get("journey-date"), '%m/%d/%Y') + timedelta(
            days=to_confirmed.total_time // 24)
        arrive_time = arrive_time.strftime('%Y/%m/%d') + ' ' + to_confirmed.landing_time.strftime('%H:%M')
        return render_template("flight-booking-confirm.html", flight=to_confirmed, customer=customer,
                               order_date=order_date, arrive_time=arrive_time, logged=True)
    else:
        url = request.referrer
        return render_template("SignInUp.html", url=url)


@bp.route("/order-success")
def order_success():
    customer = Customer.query.get(session.get("customer_id"))
    cost = float(request.args.get("cost"))
    if customer.wallet >= cost:
        flight_order = FlightOrder()
        flight_order.customerID = session.get('customer_id')
        flight_order.purchased = True
        flight_order.startTime = datetime.datetime.now()
        end_date = request.args.get("date")
        try:
            date_format = "%Y/%m/%d"
            datetime_obj = datetime.datetime.strptime(end_date, date_format)
        except ValueError:
            date_format = "%m/%d/%Y"
            datetime_obj = datetime.datetime.strptime(end_date, date_format)
        flight_order.endTime = datetime_obj
        flight_order.productID = request.args.get("flight_id")
        flight_order.cost = cost
        customer.wallet = customer.wallet - cost
        one_hour_ago = datetime.datetime.now() - timedelta(hours=1)
        last_order = FlightOrder.query.filter_by(customerID=customer.id, productID=flight_order.productID).filter(
            FlightOrder.startTime >= one_hour_ago).all()
        if len(last_order) == 0:
            db.session.add(flight_order)
            db.session.commit()
        return render_template("booking-success.html", name=request.args.get("name"), logged=True)
    else:
        flash("Insufficient balance in your wallet, please top up first")
        return redirect(url_for('customer.profile', page='/wallet'))


@bp.route('/flight_filter', methods=['GET', 'POST'])
def flight_filter():
    class_type = request.form.get('class_type').split(",")
    to_sort = request.form.get('sort_by')
    if 'language' in session:
        if session.get("language") == 'zh':
            key_word = request.form.get('key-word')
            key_word = translator(key_word, 'zh', 'en')
        else:
            key_word = request.form.get('key-word')
    else:
        key_word = request.form.get('key-word')
    if class_type[0] == '':
        class_type = ['Economy', 'Business', 'First Class']
    flight_price = request.form.get('flightPrice')
    flight_price = flight_price.split(',')
    min_price = int(flight_price[0])
    max_price = int(flight_price[-1])
    airline = request.form.get('flight-airline').split(",")
    if airline[0] == '':
        airline = ['American Airlines', 'Delta Airlines', 'Qatar Airways', 'Fly Amirates', 'Singapore Airlines']
    stop = request.form.get('flight-stop').split(",")
    if stop[0] == '':
        stop = ['Non Stop', '1 Stop', '2 Stop', '3 Stop', 'Multi Stop']
    refundable = request.form.get('flight-refundable').split(",")
    if refundable[0] == '':
        refundable = ['Refundable', 'Partially Refundable', 'Non Refundable']
    dep_time = request.form.get('dep_time').split(",")
    if dep_time[0] == '':
        dep_time_s = time(0, 0)
        dep_time_e = time(23, 59)
        queries = Flight.query.filter(
            Flight.company.in_(airline),
            Flight.flight_stop.in_(stop),
            Flight.fare_type.in_(refundable),
            Flight.flight_class.in_(class_type),
            Flight.price.between(min_price, max_price),
            Flight.takeoff_time.between(dep_time_s, dep_time_e)
        )

    else:
        filters = []
        if "00:00-05:59" in dep_time:
            filters.append(Flight.takeoff_time.between(time(0, 0), time(5, 59)))
        if "06:00-11:59" in dep_time:
            filters.append(Flight.takeoff_time.between(time(6, 0), time(11, 59)))
        if "12:00-17:59" in dep_time:
            filters.append(Flight.takeoff_time.between(time(12, 0), time(17, 59)))
        if "18:00-23:59" in dep_time:
            filters.append(Flight.takeoff_time.between(time(18, 0), time(23, 59)))
        queries = Flight.query.filter(
            Flight.company.in_(airline),
            Flight.flight_stop.in_(stop),
            Flight.fare_type.in_(refundable),
            Flight.flight_class.in_(class_type),
            Flight.price.between(min_price, max_price),
            or_(*filters)
        )
    page = int(request.form.get('page'))
    pagination = queries.paginate(page=page, per_page=18)
    flights = pagination.items
    for flight_i in flights:
        flight_i.contact_name = url_for('flight.flightDetail', flight_id=flight_i.id)
        flight_i.images = json.loads(flight_i.images)['images']
        flight_i.images[0] = "../" + flight_i.images[0][flight_i.images[0].index('static'):].replace('\\', '/')
    if to_sort == '1':
        flights = sorted(flights, key=lambda flight: flight.priority, reverse=True)

    if to_sort == '2':
        flights = sorted(flights, key=lambda flight: flight.view_num, reverse=True)

    if to_sort == '3':
        flights = sorted(flights, key=lambda flight: flight.price, reverse=False)
    if to_sort == '4':
        flights = sorted(flights, key=lambda flight: flight.price, reverse=True)

    flights = [flight.to_dict() for flight in flights]
    return jsonify({"flights": flights, "page": 1, "keyword": key_word})


@bp.route("/add_wishlist/<flight_id>")
def add_wishlist(flight_id):
    aimed_flight = Flight.query.get(flight_id)
    flight_order = FlightOrder()
    flight_order.cost = aimed_flight.price
    flight_order.startTime = datetime.datetime.now()
    flight_order.purchased = False
    flight_order.customerID = session.get("customer_id")
    flight_order.productID = flight_id
    db.session.add(flight_order)
    db.session.commit()
    return redirect(url_for('customer.profile', page="/wishlist"))


@bp.route("/remove_wishlist/<flight_id>")
def remove_wishlist(flight_id):
    flight_order = FlightOrder.query.filter_by(customerID=session.get("customer_id"), productID=flight_id,
                                               purchased=False).first()
    db.session.delete(flight_order)
    db.session.commit()
    return redirect(url_for('customer.profile', page="/wishlist"))


@bp.route('/add_review', methods=['POST'])
def add_review():
    flight_id = request.form.get('productId')
    customer_id = session.get('customer_id')
    content = request.form.get('content')
    flight = Flight.query.get(flight_id)
    flight.review_num = flight.review_num + 1
    star = int(request.form.get("rating"))
    star_index = star - 1
    star_detail = json.loads(flight.star_detail)["star_detail"]
    star_detail[star_index] = star_detail[star_index] + star
    flight.star_detail = json.dumps({"star_detail": star_detail})
    review = FlightReview(rating=star, issueTime=datetime.datetime.now(), content=content, customerID=customer_id,
                          productID=flight_id)
    db.session.add(review)
    db.session.commit()
    return redirect(url_for('flight.flightDetail', flight_id=int(flight_id)))
