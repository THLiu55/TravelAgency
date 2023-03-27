from flask import Blueprint, render_template

bp = Blueprint("manager", __name__, url_prefix="/manager")


@bp.route('/')
def manager_homepage():
    return render_template('attractions.html')