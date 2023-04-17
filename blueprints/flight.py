import json

from flask import Blueprint, session, render_template, request, url_for, redirect
from model import Flight, FlightOrder, FlightReview, Customer, Activity, ActivityOrder
import datetime
from exts import db

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
    purchased = ActivityOrder.query.filter_by(customerID=session.get("customer_id"),
                                              productID=flight_id, purchased=True).first()
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
