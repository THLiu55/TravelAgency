from flask import Blueprint, render_template, request, jsonify, current_app
from model import *
from exts import db, mail
import os
import json

bp = Blueprint("activity", __name__, url_prefix="/activity")


@bp.route("/add_activity", methods=['POST'])
def add_activity():
    activity = Activity()
    activity.name = request.form.get('name')
    activity.category = request.form.get('category')
    activity.price = request.form.get('price')
    activity.city = request.form.get('city')
    activity.state = request.form.get('state')
    activity.address = request.form.get('address')
    activity.duration = request.form.get('duration')
    activity.group_size = request.form.get('group_size')
    activity.start_time = request.form.get('start_time')
    activity.end_time = request.form.get('end_time')
    activity.description = request.form.get('description')
    activity.openHour = request.form.get('openHour')
    activity.visitHour = request.form.get('visitHour')
    included1 = request.form.get('included1')
    included2 = request.form.get('included2')
    included3 = request.form.get('included3')
    included4 = request.form.get('included4')
    not_included1 = request.form.get('not-included1')
    not_included2 = request.form.get('not-included2')
    not_included3 = request.form.get('not-included3')
    not_included4 = request.form.get('not-included4')
    activity.included = {'included': [included1, included2, included3, included4]}
    activity.excluded = {'not_included': [not_included1, not_included2, not_included3, not_included4]}
    images = request.files.getlist('images')
    max_id = db.session.query(db.func.max(Activity.id)).scalar()
    if max_id is None:
        max_id = 0
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
    activity.images = {'images': img_routes}
    activity.total_star = 0
    activity.review_num = 0
    activity.star_detail = {'star_detail': []}
    activity.contact_name = request.form.get('contact_name')
    activity.contact_email = request.form.get('contact_email')
    activity.contact_phone = request.form.get('contact_phone')

    return jsonify({'code': 200})
