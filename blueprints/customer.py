from flask import Blueprint, render_template, request, jsonify
from model import *
from werkzeug.security import generate_password_hash, check_password_hash
from exts import db, mail
from flask_mail import Message
from generate_hash import check_hash_time, get_hash_time

bp = Blueprint("customer", __name__, url_prefix="/")


@bp.route('/', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("SignInUp.html")
    else:
        customer_email = request.form.get('staff-name')
        customer_password = request.form.get('staff-password')
        return render_template("SignInUp.html")


@bp.route('/register', methods=['POST'])
def register():
    captcha_number = request.form.get('')
    email = request.form.get('email')
    if captcha_number == check_hash_time(email, captcha_number):
        pass


    return


@bp.route('/captcha', methods=['POST'])
def captcha():
    email = request.values.get("email")
    captcha_number = get_hash_time(email)
    message = Message(subject="Verify Code",
                      recipients=[email],
                      body=f"Your verify code is: {captcha_number}\t (valid for an hour)"
                           f"\nIgnore it please if this is not your own operation"
                      )
    mail.send(message)
    return jsonify({"code": 200})
