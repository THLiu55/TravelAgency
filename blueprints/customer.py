import os.path
from datetime import datetime, timedelta
import json

import requests
from flask import Blueprint, flash, render_template, request, jsonify, redirect, url_for, g, session, current_app
from model import *
from werkzeug.security import generate_password_hash, check_password_hash
from exts import db, mail, socketio
from flask_mail import Message
from utils.generate_hash import check_hash_time, get_hash_time
from flask_babel import Babel, gettext as _, refresh
from utils.decorators import login_required
from recognize import main
from translations.translator import translator
from sqlalchemy.exc import IntegrityError
from utils.toys import (
    get_cipher,
    decrypt_cdkey,
    validate_decrypted_attrs,
)

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
bp = Blueprint("customer", __name__, url_prefix="/")


@bp.route("/get_lang", methods=["POST"])
def get_language():
    session.setdefault("language", "en")
    lang = session.get("language", "en")
    return jsonify({"code": 200, "lang": lang})


@bp.route("/switch_lang", methods=["POST"])
def lang_switch():
    lang = request.form.get("lang")
    session["language"] = lang
    return jsonify({"code": 200})


@bp.route("/", methods=["GET", "POST"])
def homepage():
    logged = False if session.get('customer_id') is None else True
    total_activities = Activity.query.count()
    paginationActivity = Activity.query.paginate(page=int(1), per_page=9, error_out=False)
    activities = paginationActivity.items
    for activity in activities:
        # noinspection PyTypeChecker
        activity.images = json.loads(activity.images)['images']
        activity.images[0] = activity.images[0][activity.images[0].index('static'):].lstrip('static')

    total_flights = Flight.query.count()
    paginationFlight = Flight.query.paginate(page=int(1), per_page=9, error_out=False)
    flights = paginationFlight.items
    for flight in flights:
        # noinspection PyTypeChecker
        flight.images = json.loads(flight.images)['images']
        flight.images[0] = flight.images[0][flight.images[0].index('static'):].lstrip('static')

    total_hotels = Hotel.query.count()
    paginationHotel = Hotel.query.paginate(page=int(1), per_page=9, error_out=False)
    hotels = paginationHotel.items
    for hotel in hotels:
        # noinspection PyTypeChecker
        hotel.images = json.loads(hotel.images)['images']
        hotel.images[0] = hotel.images[0][hotel.images[0].index('static'):].lstrip('static')

    total_tours = Tour.query.count()
    paginationTour = Tour.query.paginate(page=int(1), per_page=9, error_out=False)
    tours = paginationTour.items
    for tour in tours:
        # noinspection PyTypeChecker
        tour.images = json.loads(tour.images)['images']
        tour.images[0] = tour.images[0][tour.images[0].index('static'):].lstrip('static')
    return render_template("Homepage.html", total_activities=total_activities, activities=activities,
                           total_flights=total_flights, flights=flights, total_hotels=total_hotels, hotels=hotels,
                           total_tours=total_tours, tours=tours,
                           logged=logged)


@bp.route("/getLocation", methods=["GET", "POST"])
def get_location():
    return render_template('get_lan_lat.html')


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('customer.login'))


@bp.route("/re_jump")
def re_jump():
    url = request.referrer
    return render_template('SignInUp.html', url=url)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        url = request.args.get('url')
        return render_template("SignInUp.html", url=url)
    else:
        customer_email = request.form.get("signin-email")
        customer_password = request.form.get("signin-password")
        customer = Customer.query.filter_by(email=customer_email).first()
        if customer is None:
            return jsonify({"message": "用户不存在"})
        if check_password_hash(customer.password, customer_password):
            session['customer_id'] = customer.id
            try:
                session.pop("staff_id")
            except:
                pass
            print(session['customer_id'])
            url = request.form.get("url")
            if url != "None":
                return jsonify({"code": 200, "message": url})
            else:
                return jsonify({"code": 200, "message": "/"})
        else:
            return jsonify({"message": "The email address does not match the password"})


@bp.route("/register", methods=["POST"])
def register():
    email = request.values.get("signup-email")
    captcha_number = request.form.get("signup-captcha")
    if not check_hash_time(email, captcha_number):
        return jsonify({"code": 400, "message": "captcha wrong"})
    password = request.form.get("signup-password")
    nickname = request.form.get("signup-username")
    if check_nickname_legality(nickname):
        new_customer = Customer()
        new_customer.email = email
        new_customer.nickname = nickname
        new_customer.password = generate_password_hash(password)
        new_customer.join_date = datetime.now()
        new_customer.wallet = 0
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({"code": 200})
    else:
        return jsonify({"code": 400, "message": "nickname illegal"})

def check_nickname_legality(nickname):
    if nickname in ["", None, " ", ADMIN_USERNAME]:
        return False
    elif (len(nickname) > 20):
        return False
    return True

@bp.route("/captcha", methods=["POST"])
def captcha():
    email = request.values.get("email")
    if Customer.query.filter_by(email=email).first():
        return jsonify({"code": 400, "message": "registered email"})
    captcha_number = get_hash_time(email)
    message = Message(
        sender=("Travel Agency", current_app.config.get("MAIL_USERNAME")),
        subject="Verify Code",
        recipients=[email],
        body=f"Your verify code is: {captcha_number}\t (valid for an hour)"
             f"\nIgnore it please if this is not your own operation",
    )
    mail.send(message)
    print(captcha_number)
    return jsonify({"code": 200})


@bp.route("/recaptcha", methods=["POST"])
def recaptcha():
    email = request.form.get("email")
    if not Customer.query.filter_by(email=email).first():
        return jsonify({"code": 401})
    captcha_number = get_hash_time(email)
    message = Message(
        sender=("Travel Agency", current_app.config.get("MAIL_USERNAME")),
        subject="Verify Code",
        recipients=[email],
        body=f"Your verify code is: {captcha_number}\t (valid for an hour)"
             f"\nIgnore it please if this is not your own operation",
    )
    mail.send(message)
    return jsonify({"code": 200})


@bp.route("/user/findPassword", methods=["POST"])
def resetPassword():
    email = request.form.get("email")
    captcha_number = request.form.get("captcha")
    if not check_hash_time(email, captcha_number):
        return jsonify({"code": 400, "message": "captcha wrong"})
    password = request.form.get("password")
    customer = Customer.query.filter_by(email=email).first()
    customer.password = generate_password_hash(password)
    db.session.commit()
    return jsonify({"code": 200})


@bp.route("/profile")
@login_required
def profile():
    customer = Customer.query.get(session.get('customer_id'))
    customer.join_date = customer.join_date.strftime("%Y-%m-%d %H:%M")
    page = request.args.get("page")
    if page is not None:
        page = page
    else:
        page = "/profilepage"
    return render_template("profile-base.html", customer=customer, logged=True, page=page)


@bp.route("/profilepage")
def profilepage():
    customer = Customer.query.get(session.get('customer_id'))
    customer.join_date = customer.join_date.strftime("%Y-%m-%d %H:%M")
    return render_template("profile.html", customer=customer, logged=True)


@bp.route("/plan_events_wishlist", methods=["GET"])
def plan_events_wishlist(flightlist, hotelList, tourList, activityList):
    customer = Customer.query.get(session.get('customer_id'))
    hotel_orders = HotelOrder.query.filter_by(customerID=customer.id, purchased=True, deleted=False).all()
    tour_orders = TourOrder.query.filter_by(customerID=customer.id, purchased=True, deleted=False).all()
    activity_orders = ActivityOrder.query.filter_by(customerID=customer.id, purchased=True, deleted=False).all()
    plan_list = []
    for hotel_i in hotel_orders:
        plan_object = PlanObj()
        plan_object.title = Hotel.query.get(hotel_i.productID).name
        if hotel_i.startTime > datetime.now():
            plan_object.color = '#00671'
        else:
            plan_object.color = '#ea5050'
        plan_object.start = hotel_i.startTime
        plan_object.end = hotel_i.checkOutTime
        plan_list.append(plan_object)
    for tour_i in tour_orders:
        tour_obj = Tour.query.get(tour_i.productID)
        plan_object = PlanObj()
        plan_object.title = Tour.query.get(tour_i.productID).name
        if tour_i.endTime > datetime.now():
            plan_object.color = '#009378'
        else:
            plan_object.color = '#ea5050'
        plan_object.start = tour_i.endTime
        plan_object.end = tour_i.endTime + timedelta(days=tour_obj.duration)
        plan_list.append(plan_object)
    for activity_i in activity_orders:
        plan_object = PlanObj()
        plan_object.title = Activity.query.get(activity_i.productID).name
        if activity_i.endTime > datetime.now():
            plan_object.color = '#2bb3c0'  # #e16123
        else:
            plan_object.color = '#ea5050'
        plan_object.start = activity_i.endTime
        plan_object.end = activity_i.endTime
        plan_list.append(plan_object)

    for flight_i in flightlist:
        plan_object = PlanObj()
        plan_object.title = flight_i.flightNumber
        if flight_i.endTime > datetime.now():
            plan_object.color = '#e16123'
        else:
            plan_object.color = '#ea5050'
        plan_object.start = flight_i.endTime
        plan_object.end = flight_i.endTime
        plan_list.append(plan_object)
    for hotel_i in hotelList:
        plan_object = PlanObj()
        plan_object.title = Hotel.query.get(hotel_i.productID).name
        if hotel_i.startTime > datetime.now():
            plan_object.color = '#00671'
        else:
            plan_object.color = '#ea5050'
        plan_object.start = hotel_i.startTime
        plan_object.end = hotel_i.checkOutTime
        plan_list.append(plan_object)
    for tour_i in tourList:
        tour_obj = Tour.query.get(tour_i.productID)
        plan_object = PlanObj()
        plan_object.title = Tour.query.get(tour_i.productID).name
        if tour_i.endTime > datetime.now():
            plan_object.color = '#009378'
        else:
            plan_object.color = '#ea5050'
        plan_object.start = tour_i.endTime
        plan_object.end = tour_i.endTime + timedelta(days=tour_obj.duration)
        print(plan_object.start, plan_object.end)
        plan_list.append(plan_object)
    for activity_i in activityList:
        plan_object = PlanObj()
        plan_object.title = Activity.query.get(activity_i.productID).name
        if activity_i.endTime > datetime.now():
            plan_object.color = '#2bb3c0'  # #e16123
        else:
            plan_object.color = '#ea5050'
        plan_object.start = activity_i.endTime
        plan_object.end = activity_i.endTime
        plan_list.append(plan_object)
    plan_dict_list = [plan_obj_serializer(p) for p in plan_list]
    json_data = json.dumps(plan_dict_list)
    print(json_data, "-----------------")

    return jsonify(json.loads(json_data))


@bp.route("/plan_events")
def plan_events():
    customer = Customer.query.get(session.get('customer_id'))
    hotel_orders = HotelOrder.query.filter_by(customerID=customer.id, purchased=True, deleted=False).all()
    tour_orders = TourOrder.query.filter_by(customerID=customer.id, purchased=True, deleted=False).all()
    activity_orders = ActivityOrder.query.filter_by(customerID=customer.id, purchased=True, deleted=False).all()
    flight_orders = FlightOrder.query.filter_by(customerID=customer.id, purchased=True, deleted=False).all()
    plan_list = []
    for hotel_i in hotel_orders:
        plan_object = PlanObj()
        plan_object.title = Hotel.query.get(hotel_i.productID).name
        if hotel_i.startTime > datetime.now():
            plan_object.color = '#00671'
        else:
            plan_object.color = '#ea5050'
        plan_object.start = hotel_i.startTime
        plan_object.end = hotel_i.checkOutTime
        plan_list.append(plan_object)
    for tour_i in tour_orders:
        tour_obj = Tour.query.get(tour_i.productID)
        plan_object = PlanObj()
        plan_object.title = Tour.query.get(tour_i.productID).name
        if tour_i.endTime > datetime.now():
            plan_object.color = '#009378'
        else:
            plan_object.color = '#ea5050'
        plan_object.start = tour_i.endTime
        plan_object.end = tour_i.endTime + timedelta(days=tour_obj.duration)
        plan_list.append(plan_object)
    for activity_i in activity_orders:
        plan_object = PlanObj()
        plan_object.title = Activity.query.get(activity_i.productID).name
        if activity_i.endTime > datetime.now():
            plan_object.color = '#2bb3c0'
        else:
            plan_object.color = '#ea5050'
        plan_object.start = activity_i.endTime
        plan_object.end = activity_i.endTime
        plan_list.append(plan_object)
    for flight_i in flight_orders:
        plan_object = PlanObj()
        flight_obj = Flight.query.get(flight_i.productID)
        plan_object.title = flight_obj.departure + '-' + flight_obj.destination
        if flight_i.endTime > datetime.now():
            plan_object.color = '#e16123'
        else:
            plan_object.color = '#ea5050'
        plan_object.start = flight_i.startTime
        days, hours = divmod(flight_obj.total_time, 24)
        plan_object.end = flight_i.startTime + timedelta(days=days, hours=hours)
        plan_list.append(plan_object)
    plan_dict_list = [plan_obj_serializer(p) for p in plan_list]
    json_data = json.dumps(plan_dict_list)

    return jsonify(json.loads(json_data))


def plan_obj_serializer(plan_obj):
    return {
        'title': plan_obj.title,
        'start': plan_obj.start.isoformat(),
        'end': plan_obj.end.isoformat(),
        'color': plan_obj.color
    }


@bp.route("/booking")
def booking():
    customer = Customer.query.get(session.get('customer_id'))
    hotel_orders = HotelOrder.query.filter_by(customerID=customer.id, purchased=True, deleted=False).all()
    tour_orders = TourOrder.query.filter_by(customerID=customer.id, purchased=True, deleted=False).all()
    activity_orders = ActivityOrder.query.filter_by(customerID=customer.id, purchased=True, deleted=False).all()
    flight_orders = FlightOrder.query.filter_by(customerID=customer.id, purchased=True, deleted=False).all()
    order_list = []
    for hotel_i in hotel_orders:
        order_object = OrderObject()
        order_object.price = hotel_i.cost
        order_object.name = Hotel.query.get(hotel_i.productID).name
        order_object.type = 'Hotel'
        order_object.url = url_for('hotel.hotelDetail', hotel_id=hotel_i.productID)
        order_object.status = True if hotel_i.checkOutTime < datetime.now() else False
        order_object.time = hotel_i.endTime.strftime('%y-%m-%d %H:%M')
        order_list.append(order_object)
    for tour_i in tour_orders:
        order_object = OrderObject()
        order_object.price = tour_i.cost
        order_object.name = Tour.query.get(tour_i.productID).name
        order_object.type = 'Tour'
        order_object.url = url_for('tour.tourDetail', tour_id=tour_i.productID)
        order_object.status = True if tour_i.endTime < datetime.now() else False
        order_object.time = tour_i.startTime.strftime('%y-%m-%d %H:%M')
        order_list.append(order_object)
    for activity_i in activity_orders:
        order_object = OrderObject()
        order_object.price = activity_i.cost
        order_object.name = Activity.query.get(activity_i.productID).name
        order_object.type = 'Activity'
        order_object.url = url_for('activity.activityDetail', activity_id=activity_i.productID)
        order_object.status = True if activity_i.endTime < datetime.now() else False
        order_object.time = activity_i.startTime.strftime('%y-%m-%d %H:%M')
        order_list.append(order_object)
    for flight_i in flight_orders:
        order_object = OrderObject()
        order_object.price = flight_i.cost
        flight_obj = Flight.query.get(flight_i.productID)
        order_object.name = flight_obj.departure + ' - ' + flight_obj.destination
        order_object.type = 'Flight'
        order_object.url = url_for('flight.flightDetail', flight_id=flight_i.productID)
        order_object.status = True if flight_i.endTime < datetime.now() else False
        order_object.time = flight_i.startTime.strftime('%y-%m-%d %H:%M')
        order_list.append(order_object)
    sorted_orders = sorted(order_list, key=lambda obj: obj.time, reverse=True)
    length = len(sorted_orders)
    return render_template("profile-booking.html", sorted_orders=sorted_orders, customer=customer, logged=True,
                           length=length)


@bp.route("/wishlist")
def wishlist():
    customer = Customer.query.get(session.get('customer_id'))
    flight_orders = FlightOrder.query.filter_by(customerID=customer.id, purchased=False).all()
    hotel_orders = HotelOrder.query.filter_by(customerID=customer.id, purchased=False).all()
    tour_orders = TourOrder.query.filter_by(customerID=customer.id, purchased=False).all()
    activity_orders = ActivityOrder.query.filter_by(customerID=customer.id, purchased=False).all()
    order_list = []
    for flight_i in flight_orders:
        flight_obj = Flight.query.get(flight_i.productID)
        flight_obj.images = json.loads(flight_obj.images)['images']
        flight_obj.images[0] = flight_obj.images[0][flight_obj.images[0].index('static'):]
        order_obj = WishListObject("Flight", flight_obj.departure + " - " + flight_obj.destination, 5, "Excellent",
                                   flight_obj.review_num, flight_obj.price,
                                   flight_obj.images[0],
                                   url_for('flight.flightDetail', flight_id=flight_obj.id), flight_i.startTime,
                                   "Flight", flight_i.productID)
        order_list.append(order_obj)
    for hotel_i in hotel_orders:
        hotel_obj = Hotel.query.get(hotel_i.productID)
        hotel_obj.images = json.loads(hotel_obj.images)['images']
        hotel_obj.images[0] = hotel_obj.images[0][hotel_obj.images[0].index('static'):]
        order_object = WishListObject(hotel_obj.name, hotel_obj.address + " " + hotel_obj.city, 5, "Excellent",
                                      hotel_obj.review_num, hotel_obj.min_price, hotel_obj.images[0],
                                      url_for('hotel.hotelDetail', hotel_id=hotel_obj.id), hotel_i.endTime, "Hotel",
                                      hotel_i.id)
        order_list.append(order_object)
    for tour_i in tour_orders:
        tour_object = Tour.query.get(tour_i.productID)
        tour_object.images = json.loads(tour_object.images)['images']
        tour_object.images[0] = tour_object.images[0][tour_object.images[0].index('static'):]
        order_object = WishListObject(tour_object.name, tour_object.address + " " + tour_object.city, 5, "Excellent",
                                      tour_object.review_num, tour_object.price, tour_object.images[0],
                                      url_for('tour.tourDetail', tour_id=tour_object.id), tour_i.startTime, "Tour",
                                      tour_i.id)
        order_list.append(order_object)
    for activity_i in activity_orders:
        activity_object = Activity.query.get(activity_i.productID)
        activity_object.images = json.loads(activity_object.images)['images']
        activity_object.images[0] = activity_object.images[0][activity_object.images[0].index('static'):]
        order_object = WishListObject(activity_object.name, activity_object.address + " " + activity_object.city, 5,
                                      "Excellent", activity_object.review_num, activity_i.cost,
                                      activity_object.images[0],
                                      url_for('activity.activityDetail', activity_id=activity_i.productID),
                                      activity_i.startTime, "Activity", activity_i.productID)
        order_list.append(order_object)
    sorted_orders = sorted(order_list, key=lambda obj: obj.time, reverse=True)
    length = len(sorted_orders)
    return render_template("profile-wishlist.html", customer=customer, logged=True, sorted_orders=sorted_orders,
                           length=length)


@bp.route("/wishlist_calendar", methods=['POST', 'GET'])
def plan_wishlist():
    order_id = request.form.get("order_id")
    order_type = request.form.get("order_type")
    flightList = []
    hotelList = []
    tourList = []
    activityList = []
    if order_type == "Flight":
        order = FlightOrder.query.get(order_id)
        flightList.append(order)

    elif order_type == "Hotel":
        order = HotelOrder.query.get(order_id)
        hotelList.append(order)
    elif order_type == "Tour":
        ordertemp = TourOrder.query.get(order_id)
        temp = ordertemp.productID
        order = Tour.query.get(temp)
        tourList.append(order)
    elif order_type == "Activity":
        # ordertemp = ActivityOrder.query.get(order_id)
        # temp = ordertemp.productID
        order = Activity.query.get(order_id)
        activityList.append(order)
    # print(flightList, hotelList, tourList, activityList,"flightList, hotelList, tourList, activityList")
    customer = Customer.query.get(session.get('customer_id'))
    hotel_orders = HotelOrder.query.filter_by(customerID=customer.id, purchased=True, deleted=False).all()
    tour_orders = TourOrder.query.filter_by(customerID=customer.id, purchased=True, deleted=False).all()
    activity_orders = ActivityOrder.query.filter_by(customerID=customer.id, purchased=True, deleted=False).all()
    plan_list = []
    for hotel_i in hotel_orders:
        plan_object = PlanObj()
        plan_object.title = Hotel.query.get(hotel_i.productID).name
        if hotel_i.startTime > datetime.now():
            plan_object.color = '#00671'
        else:
            plan_object.color = '#ea5050'
        plan_object.start = hotel_i.startTime
        plan_object.end = hotel_i.checkOutTime
        plan_list.append(plan_object)
    for tour_i in tour_orders:
        tour_obj = Tour.query.get(tour_i.productID)
        plan_object = PlanObj()
        plan_object.title = Tour.query.get(tour_i.productID).name
        if tour_i.endTime > datetime.now():
            plan_object.color = '#009378'
        else:
            plan_object.color = '#ea5050'
        plan_object.start = tour_i.endTime
        plan_object.end = tour_i.endTime + timedelta(days=tour_obj.duration)
        plan_list.append(plan_object)
    for activity_i in activity_orders:
        plan_object = PlanObj()
        plan_object.title = Activity.query.get(activity_i.productID).name
        if activity_i.endTime > datetime.now():
            plan_object.color = '#2bb3c0'  # #e16123
        else:
            plan_object.color = '#ea5050'
        plan_object.start = activity_i.endTime
        plan_object.end = activity_i.endTime
        plan_list.append(plan_object)

    for hotel_ii in hotelList:
        plan_object = PlanObj()
        plan_object.title = Hotel.query.get(hotel_ii.productID).name
        if hotel_ii.startTime > datetime.now():
            plan_object.color = '#00671'
        else:
            plan_object.color = '#ea5050'
        plan_object.start = hotel_ii.startTime
        plan_object.end = hotel_ii.checkOutTime
        plan_list.append(plan_object)
    for tour_ii in tourList:
        tour_obj = Tour.query.get(tour_ii.id)
        plan_object = PlanObj()
        plan_object.title = Tour.query.get(tour_ii.id).name
        if tour_ii.start_time > datetime.now():
            plan_object.color = '#009378'
        else:
            plan_object.color = '#ea5050'
        plan_object.start = tour_ii.start_time
        plan_object.end = tour_ii.end_time + timedelta(days=tour_obj.duration)
        print(plan_object.start, plan_object.end)
        plan_list.append(plan_object)
    for activity_ii in activityList:
        plan_object = PlanObj()
        plan_object.title = Activity.query.get(activity_ii.id).name
        if activity_ii.end_time > datetime.now():
            plan_object.color = '#2bb3c0'  # #e16123
        else:
            plan_object.color = '#ea5050'
        plan_object.start = activity_ii.start_time
        plan_object.end = activity_ii.end_time
        print(plan_object.start, plan_object.end)
        plan_list.append(plan_object)

    plan_dict_list = [plan_obj_serializer(p) for p in plan_list]
    json_data = json.dumps(plan_dict_list)
    print(plan_dict_list, "-----------------")
    print(json_data, "-----------------")
    print(json.loads(json_data), "-----------------")

    return jsonify(json.loads(json_data))
    # return redirect(url_for('customer.wishlist'))


@bp.route("/wallet")
def wallet():
    customer = Customer.query.get(session.get('customer_id'))
    return render_template("profile-wallet.html", logged=True, customer=customer)


@bp.route("/top_up", methods=["POST"])
def top_up():
    cdk = request.form.get("cdk-number")
    if not cdk:
        flash("Please enter a CDK", "error")
        return redirect(url_for("customer.profile", page="wallet"))
    customer = Customer.query.get(session.get("customer_id"))
    dec_date_str, dec_serial_str, dec_value_str = "", "", ""
    # try:
    dec_date_str, dec_serial_str, dec_value_str = decrypt_cdkey(get_cipher(), cdk)
    # print("date: ", dec_date_str, "serial: ", dec_serial_str, "value: ", dec_value_str)
    if validate_decrypted_attrs(dec_date_str, dec_serial_str, dec_value_str):
        redeem_history = RedeemHistory(
            cdk_generate_date=datetime.strptime(dec_date_str, "%Y%m%d"),
            cdk_serial=int(dec_serial_str),
            cdk_value=int(dec_value_str),
            customerID=customer.id,
            redeem_time=datetime.now(),
        )
        # use try to avoid duplicate cdk
        try:
            db.session.add(redeem_history)
            customer.wallet += int(dec_value_str)
            db.session.commit()
        except IntegrityError:
            flash("CDK used", "error")
            return redirect(url_for("customer.profile", page="wallet"))
    else:
        flash("CDK invalid", "error")
    return redirect(url_for("customer.profile", page="/wallet"))


@bp.route("/setting")
def setting():
    customer = Customer.query.get(session.get('customer_id'))
    return render_template("profile-setting.html", logged=True, customer=customer)


@bp.route("/about_us")
def about_us():
    return render_template("AboutUs.html")


@bp.route("/update-profile", methods=['POST'])
@login_required
def update_profile():
    customer = Customer.query.get(session.get("customer_id"))
    nickname_to_check = request.form.get("name")
    if check_nickname_legality(nickname_to_check):
        customer.nickname = nickname_to_check
        customer.email = request.form.get("email")
        customer.phone_number = request.form.get("phone")
        customer.address = request.form.get("address")
        db.session.commit()
        return redirect(url_for('customer.profile'))
    else:
        return redirect(url_for('customer.profile', page='/setting'))


@bp.route("/recognize", methods=['POST'])
def recognize():
    name = request.form.get('category-name')
    photo = request.files['photo-to-recognize']
    if len(photo.read()) > 4194304:
        result = 'The picture size should be less than 4MB'
    else:
        result = json.loads(main(photo))['result'][0]['keyword']
    if session.get("language") != 'zh':
        result = translator(result, 'zh', 'en')
    else:
        result = result
    return redirect(url_for(name, page_num=1, result=result))
