from flask import Blueprint, render_template

bp = Blueprint("manager", __name__, url_prefix="/manager")


@bp.route('/add_activity')
def add_activity():
    return render_template('manager.html')