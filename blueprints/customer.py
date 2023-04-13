from datetime import datetime

import requests
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, g, session, current_app
from model import *
from werkzeug.security import generate_password_hash, check_password_hash
from exts import db, mail, socketio
from flask_mail import Message
from utils.generate_hash import check_hash_time, get_hash_time
from flask_babel import Babel, gettext as _, refresh
from utils.decorators import login_required

bp = Blueprint("customer", __name__, url_prefix="/")


@bp.route("/", methods=["GET", "POST"])
def homepage():
    logged = False if session.get('customer_id') is None else True
    return render_template("Homepage.html", logged=logged)


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
    new_customer = Customer()
    new_customer.email = email
    new_customer.nickname = nickname
    new_customer.password = generate_password_hash(password)
    new_customer.join_date = datetime.now()
    new_customer.wallet = 0
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"code": 200})


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


### CHAT RELATED ###
@bp.route("/consult", methods=["GET", "POST"])
def consult():
    """customer consult with staff"""
    g.customer = Customer.query.filter_by(id=1).first()
    return render_template("chat.html")


### END CHAT RELATED ###


@bp.route("/profile")
def profile():
    customer = Customer.query.get(session.get('customer_id'))
    customer.join_date = customer.join_date.strftime("%Y-%m-%d %H:%M")
    return render_template("profile-base.html", customer=customer, logged=True)


@bp.route("/profilepage")
def profilepage():
    customer = Customer.query.get(session.get('customer_id'))
    customer.join_date = customer.join_date.strftime("%Y-%m-%d %H:%M")
    return render_template("profile.html", customer=customer, logged=True)


@bp.route("/booking")
def booking():
    customer = Customer.query.get(session.get('customer_id'))
    hotel_orders = HotelOrder.query.filter_by(customerID=customer.id, purchased=True).all()
    tour_orders = TourOrder.query.filter_by(customerID=customer.id, purchased=True).all()
    activity_orders = ActivityOrder.query.filter_by(customerID=customer.id, purchased=True).all()
    order_list = []
    for hotel_i in hotel_orders:
        order_object = OrderObject()
        order_object.price = hotel_i.cost
        order_object.name = Hotel.query.get(hotel_i.productID).name
        order_object.type = 'Hotel'
        order_object.url = url_for('hotel.hotelDetail', hotel_id=hotel_i.productID)
        order_object.status = True if hotel_i.checkOutTime < datetime.now() else False
        order_object.time = hotel_i.endTime
        order_list.append(order_object)
    for tour_i in tour_orders:
        order_object = OrderObject()
        order_object.price = tour_i.cost
        order_object.name = Tour.query.get(tour_i.productID).name
        order_object.type = 'Tour'
        order_object.url = url_for('tour.tourDetail', tour_id=tour_i.productID)
        order_object.status = True if tour_i.endTime < datetime.now() else False
        order_object.time = tour_i.startTime
        order_list.append(order_object)
    for activity_i in activity_orders:
        order_object = OrderObject()
        order_object.price = activity_i.cost
        order_object.name = Activity.query.get(activity_i.productID).name
        order_object.type = 'Activity'
        order_object.url = url_for('activity.activityDetail', activity_id=activity_i.productID)
        order_object.status = True if activity_i.endTime < datetime.now() else False
        order_object.time = activity_i.startTime
        order_list.append(order_object)
    sorted_orders = sorted(order_list, key=lambda obj: obj.time)
    length = len(sorted_orders)
    return render_template("profile-booking.html", sorted_orders=sorted_orders, customer=customer, logged=True,
                           length=length)


@bp.route("/wishlist")
def wishlist():
    customer = Customer.query.get(session.get('customer_id'))
    return render_template("profile-wishlist.html", customer=customer, logged=True)


@bp.route("/wallet")
def wallet():
    customer = Customer.query.get(session.get('customer_id'))
    return render_template("profile-wallet.html", logged=True, customer=customer)


@bp.route("/setting")
def setting():
    customer = Customer.query.get(session.get('customer_id'))
    return render_template("profile-setting.html", logged=True, customer=customer)


@bp.route("/update-profile", methods=['POST'])
def update_profile():
    customer = Customer.query.get(session.get("customer_id"))
    customer.email = request.form.get("email")
    customer.nickname = request.form.get("name")
    customer.phone_number = request.form.get("phone")
    customer.address = request.form.get("address")
    db.session.commit()
    return redirect(url_for('customer.profile'))

# @bp.route("/flight")
# def flight():
#     customer = Customer.query.get(session.get('customer_id'))
#     return render_template("flight-grid.html", customer=customer, logged=True)