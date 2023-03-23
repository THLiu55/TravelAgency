














from flask import Blueprint, render_template, request, jsonify
from model import *
from exts import db, mail

bp = Blueprint("activity", __name__, url_prefix="/activity")


@bp.route("/add")
def add_activity():
    return jsonify({'code': 200})