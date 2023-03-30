import json
from datetime import datetime

from flask import Blueprint, render_template, request, jsonify, current_app, session
from model import *
from exts import db

bp = Blueprint("tour", __name__, url_prefix="/tour")


@bp.route("/<page_num>")
def tourList(page_num):
    total_tours = Tour.query.count()
    pagination = Tour.query.paginate(page=int(page_num), per_page=9, error_out=False)
    tours = pagination.items
    for single_tour in tours:
        # noinspection PyTypeChecker
        single_tour.images = json.loads(single_tour.images)['images']
        single_tour.images[0] = single_tour.images[0][single_tour.images[0].index('static'):].lstrip('static')
    return render_template("tour-grid.html", total_tours=total_tours, tours=tours)


@bp.route('/details/<tour_id>/', methods=['GET'])
def tourDetail(tour_id):
    tour = Tour.query.get(tour_id)
    if tour is None:
        return jsonify({'code': 400, 'message': "no activity found"})
    tour.included = json.loads(tour.included)['included']
    tour.included = [i for i in tour.included if i is not None]
    tour.excluded = json.loads(tour.excluded)['not_included']
    tour.excluded = [i for i in tour.excluded if i is not None]
    tour.images = json.loads(tour.images)['images']
    tour.images = [image[image.index('static'):].lstrip('static') for image in tour.images]
    return render_template("tour-detail.html", tour=tour)
