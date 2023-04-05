import json
from datetime import datetime

from flask import Blueprint, render_template, request, jsonify, current_app, session, redirect, url_for
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
    reviews = tour.review
    if tour is None:
        return jsonify({'code': 400, 'message': "no activity found"})
    tour.included = json.loads(tour.included)['included']
    tour.included = [i for i in tour.included if i is not None]
    tour.excluded = json.loads(tour.excluded)['not_included']
    tour.excluded = [i for i in tour.excluded if i is not None]
    tour.images = json.loads(tour.images)['images']
    images = [image[image.index('static'):].lstrip('static') for image in tour.images]
    tour.itineraries = json.loads(tour.itineraries)['tour_des']
    tour.itineraries = [list(i.items())[0] for i in tour.itineraries]
    tour.start_time = tour.start_time.strftime("%Y-%m-%d")
    tour.end_time = tour.end_time.strftime("%Y-%m-%d %H:%M")
    days = len(tour.itineraries)
    for review in reviews:
        review.customerID = Customer.query.get(review.customerID).nickname
        review.issueTime = review.issueTime.strftime("%Y-%m-%d %H:%M")
    tour.review_num = tour.review_num + 1
    return render_template("tour-detail.html", tour=tour, days=days, images=images, reviews=reviews)


@bp.route('/add_review', methods=['POST'])
def add_review():
    tour_id = request.form.get('productId')
    customer_id = session.get('customer_id')
    rating = int(request.form.get('rating'))
    content = request.form.get('content')
    # check if all the data have been entered
    if not customer_id or not rating or not content:
        return jsonify({'code': 400, 'message': 'Invalid data'})
    # check if activity exist
    tour = Tour.query.get(tour_id)
    if tour is None:
        return jsonify({'code': 400, 'message': 'Activity not found'})
    # check if the customer has ordered the activity
    # order = ActivityOrder.query.filter_by(customerID=customer_id, productID=activity_id).first()
    # if order is None:
    #     return jsonify({'code': 400, 'message': 'No order'})
    review = TourReview(rating=rating, issueTime=datetime.now(), content=content, customerID=customer_id,
                        productID=tour_id)
    tour.review_num = tour.review_num + 1
    db.session.add(review)
    db.session.commit()
    return redirect(url_for('tour.tourDetail', tour_id=int(tour.id)))


@bp.route('/tour_filter', methods=['GET', 'POST'])
def tour_filter():
    pass




