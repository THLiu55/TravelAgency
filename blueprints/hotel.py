import json
from datetime import datetime

from flask import Blueprint, render_template, request, jsonify, current_app, session, redirect, url_for
from model import *
from exts import db

bp = Blueprint("hotel", __name__, url_prefix="/hotel")


@bp.route("/<page_num>")
def hotelList(page_num):
    total_hotels = Hotel.query.count()
    pagination = Hotel.query.paginate(page=int(page_num), per_page=9, error_out=False)
    hotels = pagination.items
    for single_hotel in hotels:
        # noinspection PyTypeChecker
        single_hotel.images = json.loads(single_hotel.images)['images']
        single_hotel.images[0] = single_hotel.images[0][single_hotel.images[0].index('static'):].lstrip('static')
    return render_template("tour-grid.html", total_tours=total_hotels, tours=hotels)