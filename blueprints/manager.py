import json
from datetime import datetime

from flask import Blueprint, render_template, request, jsonify, current_app, session, redirect, url_for
from model import *
from exts import db
import os

bp = Blueprint("manager", __name__, url_prefix="/manager")


@bp.route('/')
def manager_homepage():
    return render_template('attractions.html')


@bp.route("/add_activity", methods=['POST'])
def add_activity():
    activity = Activity()
    activity.status = 'published'
    activity.name = request.form.get('name')
    print(request.form.get('category'))
    activity.category = request.form.get('category')
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
    return redirect(url_for('manager.activities'))


@bp.route('/delete_activity/<activity_id>', methods=['GET', 'POST'])
def delete_activity(activity_id):
    activity = Activity.query.get(activity_id)
    if activity is None:
        return jsonify({'code': 400, 'message': "no activity found"})
    activity.status = "deleted"
    db.session.commit()
    return redirect(url_for('manager.activities'))


@bp.route('/activities', methods=['GET', 'POST'])
def activities():
    db.create_all()
    page_num = 1
    page = Activity.query.paginate(page=page_num, per_page=10)
    return render_template('attractions.html', page=page)