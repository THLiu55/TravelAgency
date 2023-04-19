import json

from flask import Blueprint, session, render_template, request, url_for, redirect, jsonify
from model import Flight, FlightOrder, FlightReview, Customer, Activity, ActivityOrder
import datetime
from exts import db
from datetime import time
from sqlalchemy import or_

bp = Blueprint("flight", __name__, url_prefix="/flight")


@bp.route('/<page_num>', methods=['POST', 'GET'])
def flightList(page_num):
    logged = False if session.get('customer_id') is None else True
    total_flights = Flight.query.count()
    pagination = Flight.query.paginate(page=int(page_num), per_page=9, error_out=False)
    flights = pagination.items
    for flight in flights:
        # noinspection PyTypeChecker
        flight.images = json.loads(flight.images)['images']
        flight.images[0] = flight.images[0][flight.images[0].index('static'):].lstrip('static')
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
    return render_template("flight-detail.html", logged=logged, flight=flight, images=images, wifi=wifi,
                           air_condition=air_condition, coffee=coffee
                           , entertainment=entertainment, food=food, drink=drink, wines=wines, comfort=comfort,
                           television=television, shopping=shopping, magazines=magazines, game=game,
                           day_of_week=flight.week_day, added=added, purchased=purchased)


@bp.route("/order-confirm", methods=['POST'])
def order_confirm():
    customer_id = session.get('customer_id')
    if customer_id:
        flight_id = request.form.get("flight_id")
        to_confirmed = Flight.query.get(flight_id)
        order_date = request.form.get("journey-date")
        customer = Customer.query.get(customer_id)
        return render_template("flight-booking-confirm.html", flight=to_confirmed, customer=customer,
                               order_date=order_date, logged=True)
    else:
        url = request.referrer
        return render_template("SignInUp.html", url=url)


@bp.route("/order-success")
def order_success():
    customer = Customer.query.get(session.get("customer_id"))
    cost = float(request.args.get("cost"))
    if customer.wallet >= cost:
        activity_order = ActivityOrder()
        activity_order.customerID = session.get('customer_id')
        activity_order.purchased = True
        activity_order.startTime = datetime.datetime.now()
        end_date = request.args.get("date")
        try:
            date_format = "%Y/%m/%d"
            datetime_obj = datetime.datetime.strptime(end_date, date_format)
        except ValueError:
            date_format = "%m/%d/%Y"
            datetime_obj = datetime.datetime.strptime(end_date, date_format)
        activity_order.endTime = datetime_obj
        activity_order.productID = request.args.get("activity_id")
        activity_order.cost = cost
        customer.wallet = customer.wallet - cost
        db.session.add(activity_order)
        db.session.commit()
        return render_template("booking-success.html", name=request.args.get("name"), logged=True)
    else:
        return jsonify({"balance": 400})


@bp.route('/flight_filter', methods=['GET', 'POST'])
def flight_filter():
    class_type = request.form.get('class_type').split(",")
    to_sort = request.form.get('sort_by')
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
    pagination = queries.paginate(page=page, per_page=9)
    flights = pagination.items
    for flight_i in flights:
        flight_i.contact_name = url_for('flight.flightDetail', flight_id=flight_i.id)
        flight_i.images = json.loads(flight_i.images)['images']
        flight_i.images[0] = "../" + flight_i.images[0][flight_i.images[0].index('static'):].replace('\\', '/')
    if to_sort == '2':
        flights = sorted(flights, key=lambda flight: flight.view_num, reverse=True)

    if to_sort == '3':
        flights = sorted(flights, key=lambda flight: flight.price, reverse=False)
    if to_sort == '4':
        flights = sorted(flights, key=lambda flight: flight.price, reverse=True)

    flights = [flight.to_dict() for flight in flights]
    return jsonify({"flights": flights, "page": 1})


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
