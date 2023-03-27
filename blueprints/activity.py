import json
from datetime import datetime

from flask import Blueprint, render_template, request, jsonify, current_app, session
from model import *
from exts import db
import os

bp = Blueprint("activity", __name__, url_prefix="/activity")


@bp.route("/add_activity", methods=['GET', 'POST'])
def add_activity():
    activity = Activity()
    activity.status = 'published'
    activity.name = request.form.get('name')
    activity.category = int(request.form.get('category'))
    activity.category = 1
    activity.price = float(request.form.get('price'))
    activity.city = request.form.get('city')
    activity.state = request.form.get('state')
    activity.address = request.form.get('address')
    activity.duration = request.form.get('duration')
    activity.group_size = int(request.form.get('group_size'))
    activity.start_time = datetime.strptime(request.form.get('start_time'), '%Y-%m-%d')
    activity.end_time = datetime.strptime(request.form.get('end_time'), '%Y-%m-%d')
    activity.description = request.form.get('description')
    activity.openHour = datetime.strptime(request.form.get('openHour'), '%H:%M')
    activity.visitHour = request.form.get('visitHour')
    included1 = request.form.get('included1')
    included2 = request.form.get('included2')
    included3 = request.form.get('included3')
    included4 = request.form.get('included4')
    not_included1 = request.form.get('not-included1')
    not_included2 = request.form.get('not-included2')
    not_included3 = request.form.get('not-included3')
    not_included4 = request.form.get('not-included4')
    activity.included = json.dumps({'included': [included1, included2, included3, included4]})
    activity.excluded = json.dumps({'not_included': [not_included1, not_included2, not_included3, not_included4]})
    images = request.files.getlist('images')
    max_id = db.session.query(db.func.max(Activity.id)).scalar()
    if max_id is None:
        max_id = 1
    else:
        max_id = max_id + 1
    img_routes = []
    for image in images:
        folder_path = os.path.join(current_app.root_path, 'static', 'activity_img', str(max_id))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        save_path = os.path.join(folder_path, image.filename)
        image.save(save_path)
        img_routes.append(save_path)
    activity.images = json.dumps({'images': img_routes})
    activity.total_star = 0
    activity.review_num = 0
    activity.star_detail = json.dumps({'star_detail': []})
    activity.contact_name = request.form.get('contact_name')
    activity.contact_email = request.form.get('contact_email')
    activity.contact_phone = request.form.get('contact_phone')
    db.session.add(activity)
    db.session.commit()
    return jsonify({'code': 200})


@bp.route('/delete')
def delete_activity():
    activity_id = request.form.get('activity_id')
    activity = Activity.query.get(activity_id)
    if activity is None:
        return jsonify({'code': 400, 'message': "no activity found"})
    activity.status = "deleted"
    db.session.commit()
    return jsonify({'code': 200})


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


