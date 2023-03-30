import json
from datetime import datetime

from flask import Blueprint, render_template, request, jsonify, current_app, session
from model import *
from exts import db


bp = Blueprint("activity", __name__, url_prefix="/activity")


@bp.route('/add_review/<activity_id>', methods=['POST'])
def add_review(activity_id):
    customer_id = session.get('customer_id')
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


@bp.route('/<page_num>', methods=['GET', 'POST'])
def activityList(page_num):
    total_activities = Activity.query.count()
    pagination = Activity.query.paginate(page=int(page_num), per_page=9, error_out=False)
    activities = pagination.items
    for activity in activities:
        activity.included = json.loads(activity.included)
        activity.excluded = json.loads(activity.excluded)
        # noinspection PyTypeChecker
        activity.images = json.loads(activity.images)['images']
        activity.images = [image[image.index('static'):].lstrip('static') for image in activity.images]
    return render_template('activity-grid.html', total_activities=total_activities, activities=activities)


@bp.route('/details/<activity_id>/', methods=['GET'])
def activityDetail(activity_id):
    activity = Activity.query.get(activity_id)
    if activity is None:
        return jsonify({'code': 400, 'message': "no activity found"})
    activity.included = json.loads(activity.included)['included']
    activity.included = [i for i in activity.included if i is not None]
    activity.excluded = json.loads(activity.excluded)['not_included']
    activity.excluded = [i for i in activity.excluded if i is not None]
    activity.images = json.loads(activity.images)['images']
    activity.images = [image[image.index('static'):].lstrip('static') for image in activity.images]
    return render_template("activity-detail.html", activity=activity)


