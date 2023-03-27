import json
from datetime import datetime

from flask import Blueprint, render_template, request, jsonify, current_app, session
from model import *
from exts import db
import os

bp = Blueprint("activity", __name__, url_prefix="/activity")



@bp.route('/add_review')
def add_review():
    customer_id = session.get('customer_id')
    activity_id = request.form.get('activity_id')
    rating = request.form.get('rating')
    content = request.form.get('rating')
    # check if all the data have been entered
    if not customer_id or not rating or not content:
        return jsonify({'code': 400, 'message': 'Invalid data'})
    # check if activity exist
    activity = Activity.query.get(activity_id)
    if activity is None:
        return jsonify({'code': 400, 'message': 'Activity not found'})
    # check if the customer has ordered the activity
    order = ActivityOrder.query.filter_by(customerID=customer_id, productID=activity_id).first()
    if order is None:
        return jsonify({'code': 400, 'message': 'No order'})
    review = ActivityReview(rating=rating, issueTime=datetime.now(), content=content, customerID=customer_id,
                            productID=activity_id)
    db.session.add(review)
    db.session.commit()
    return jsonify({'code': 200})


@db.route('/<page_num>', methods=['GET', 'POST'])
def activityList(page_num):
