from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from model import *
from werkzeug.security import generate_password_hash, check_password_hash
from exts import db, mail
from flask_mail import Message
from utils.generate_hash import check_hash_time, get_hash_time
from flask_babel import Babel, gettext as _, refresh


bp = Blueprint("customer", __name__, url_prefix="/")


@bp.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template("Homepage.html")


@bp.route('/login', methods=['GET', 'POST'])
def login():
    customer_email = request.form.get('signin-email')
    customer_password = request.form.get('signin-password')
    customer = Customer.query.filter_by(email=customer_email).first()
    if check_password_hash(customer.password, customer_password):
        return jsonify({'code': 200})
    else:
        return jsonify({'message': 'The email address does not match the password'})


@bp.route('/register', methods=['POST'])
def register():
    email = request.values.get('signup-email')
    captcha_number = request.form.get('signup-captcha')
    if not check_hash_time(email, captcha_number):
        return jsonify({'code': 400, 'message': 'captcha wrong'})
    password = request.form.get('signup-password')
    nickname = request.form.get('signup-username')
    new_customer = Customer()
    new_customer.email = email
    new_customer.nickname = nickname
    new_customer.password = generate_password_hash(password)
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'code': 200})


@bp.route('/captcha', methods=['POST'])
def captcha():
    email = request.values.get("email")
    if Customer.query.filter_by(email=email).first():
        return jsonify({"code": '400', 'msg': 'registered email'})
    captcha_number = get_hash_time(email)
    message = Message(
        sender=('Travel Agency', '316710519@qq.com'),
        subject="Verify Code",
        recipients=[email],
        body=f"Your verify code is: {captcha_number}\t (valid for an hour)"
             f"\nIgnore it please if this is not your own operation"
    )
    mail.send(message)
    return jsonify({"code": 200})


@bp.route('/recaptcha', methods=['POST'])
def recaptcha():
    email = request.form.get("email")
    if not Customer.query.filter_by(email=email).first():
        return jsonify({"code": 401})
    captcha_number = get_hash_time(email)
    message = Message(
        sender=('Travel Agency', '316710519@qq.com'),
        subject="Verify Code",
        recipients=[email],
        body=f"Your verify code is: {captcha_number}\t (valid for an hour)"
             f"\nIgnore it please if this is not your own operation"
    )
    mail.send(message)
    return jsonify({"code": 200})


@bp.route('/user/findPassword', methods=['POST'])
def resetPassword():
    email = request.form.get('email')
    captcha_number = request.form.get('captcha')
    if not check_hash_time(email, captcha_number):
        return jsonify({'code': 400, 'message': 'captcha wrong'})
    password = request.form.get('password')
    customer = Customer.query.filter_by(email=email).first()
    customer.password = generate_password_hash(password)
    db.session.commit()
    return jsonify({'code': 200})

