import json
from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    current_app,
    session,
    redirect,
    url_for,
    g,
)
from model import *
from exts import db
import os

bp = Blueprint("manager", __name__, url_prefix="/manager")


@bp.route("/")
def manager_homepage():
    return render_template("manager.html")

# @bp.route('/destination', methods=["POST"])
# def destinationList():
#     return render_template("destinations.html")

@bp.route("/load_activities", methods=["POST"])
def load_activities():
    category = request.form.get("category")
    status = request.form.get("publish")
    q = Activity.query
    print(status)
    if category != "All Category":
        q = q.filter_by(category=category)
    if status != "All Status":
        q = q.filter_by(status=status)
    activities = [activity.serialize() for activity in q.all()]
    return jsonify({"code": 200, "content": activities})


@bp.route("/add_activity", methods=["POST"])
def add_activity():
    activity = Activity()
    activity.status = "published"
    activity.name = request.form.get("name")
    activity.category = request.form.get("category")
    activity.price = float(request.form.get("price"))
    activity.city = request.form.get("city")
    activity.state = request.form.get("state")
    activity.address = request.form.get("address")
    activity.duration = request.form.get("duration")
    activity.group_size = int(request.form.get("group_size"))
    activity.start_time = datetime.strptime(request.form.get("start_time"), "%Y-%m-%d")
    activity.end_time = datetime.strptime(request.form.get("end_time"), "%Y-%m-%d")
    activity.description = request.form.get("description")
    activity.openHour = datetime.strptime(request.form.get("openHour"), "%H:%M")
    activity.visitHour = request.form.get("visitHour")
    # noinspection DuplicatedCode
    included1 = request.form.get("included1")
    included2 = request.form.get("included2")
    included3 = request.form.get("included3")
    included4 = request.form.get("included4")
    not_included1 = request.form.get("not-included1")
    not_included2 = request.form.get("not-included2")
    not_included3 = request.form.get("not-included3")
    not_included4 = request.form.get("not-included4")
    activity.included = json.dumps(
        {"included": [included1, included2, included3, included4]}
    )
    activity.excluded = json.dumps(
        {"not_included": [not_included1, not_included2, not_included3, not_included4]}
    )
    images = request.files.getlist("images")
    max_id = db.session.query(db.func.max(Activity.id)).scalar()
    if max_id is None:
        max_id = 1
    else:
        max_id = max_id + 1
    img_routes = []
    for image in images:
        folder_path = os.path.join(
            current_app.root_path, "static", "activity_img", str(max_id)
        )
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        save_path = os.path.join(folder_path, image.filename)
        image.save(save_path)
        img_routes.append(save_path)
    activity.images = json.dumps({"images": img_routes})
    activity.total_star = 0
    activity.review_num = 0
    activity.star_detail = json.dumps({"star_detail": []})
    activity.contact_name = request.form.get("contact_name")
    activity.contact_email = request.form.get("contact_email")
    activity.contact_phone = request.form.get("contact_phone")
    db.session.add(activity)
    db.session.commit()
    return redirect(url_for("manager.activities"))


@bp.route('/delete_activity', methods=['GET', 'POST'])
def delete_activity():
    activity_id = request.form.get('id')
    activity = Activity.query.get(activity_id)
    if activity is None:
        return jsonify({'code': 400, 'message': "no activity found"})
    activity.status = "deleted"
    db.session.commit()
    return redirect(url_for('manager.activities'))


@bp.route('/activities', methods=['GET', 'POST'])
def activities():
    return render_template("activities.html")


### CHAT RELATED ###
@bp.route("/responding/<target_customer_id>/", methods=["GET", "POST"])
def respond_to(target_customer_id):
    """manager bargaining with target customer

    Args:
        targetcustomer_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    # target_user = Customer.query.filter_by(id=target_customer_id).first()
    # if target_user == None:
    #     return False
    # manager = g.admin
    # TODO: finish this function
    return render_template("chat.html")


### END CHAT RELATED ###


@bp.route("/add_tour", methods=["GET", "POST"])
def add_tour():
    tour = Tour()
    tour.status = "published"
    tour.name = request.form.get("name")
    tour.category = request.form.get("category")
    tour.price = float(request.form.get("price"))
    tour.city = request.form.get("city")
    tour.state = request.form.get("state")
    tour.address = request.form.get("address")
    tour.duration = request.form.get("duration")
    tour.group_size = int(request.form.get("group_size"))
    tour.start_time = datetime.strptime(request.form.get("start_time"), "%Y-%m-%d")
    tour.end_time = datetime.strptime(request.form.get("end_time"), "%Y-%m-%d")
    tour.description = request.form.get("description")
    # noinspection DuplicatedCode
    included1 = request.form.get("included1")
    included2 = request.form.get("included2")
    included3 = request.form.get("included3")
    included4 = request.form.get("included4")
    not_included1 = request.form.get("not-included1")
    not_included2 = request.form.get("not-included2")
    not_included3 = request.form.get("not-included3")
    not_included4 = request.form.get("not-included4")
    tour.included = json.dumps(
        {"included": [included1, included2, included3, included4]}
    )
    tour.excluded = json.dumps(
        {"not_included": [not_included1, not_included2, not_included3, not_included4]}
    )
    images = request.files.getlist("images")
    max_id = db.session.query(db.func.max(Tour.id)).scalar()
    if max_id is None:
        max_id = 1
    else:
        max_id = max_id + 1
    img_routes = []
    for image in images:
        folder_path = os.path.join(
            current_app.root_path, "static", "tour_img", str(max_id)
        )
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        save_path = os.path.join(folder_path, image.filename)
        image.save(save_path)
        img_routes.append(save_path)
    tour.images = json.dumps({"images": img_routes})
    tour.total_star = 0
    tour.review_num = 0
    tour.star_detail = json.dumps({"star_detail": []})
    tour.contact_name = request.form.get("contact_name")
    tour.contact_email = request.form.get("contact_email")
    tour.contact_phone = request.form.get("contact_phone")
    days = int(tour.duration)
    des = []
    i = 1
    while i <= days:
        des.append({request.form.get("itinerary_name_{day}".format(day=i)): request.form.get(
            "itinerary_desc_{day}".format(day=i))})
        i = i + 1
    tour.itineraries = json.dumps({"tour_des": des})
    db.session.add(tour)
    db.session.commit()
    return redirect(url_for("manager.tours"))


@bp.route("/load_tours", methods=["POST"])
def load_tours():
    category = request.form.get("category")
    status = request.form.get("publish")
    q = Tour.query
    if category != "All Category":
        q = q.filter_by(category=category)
    if status != "All Status":
        q = q.filter_by(status=status)
    tours = [tour.serialize() for tour in q.all()]
    return jsonify({"code": 200, "content": tours})


@bp.route('/delete_tour', methods=['GET', 'POST'])
def delete_tour():
    tour_id = request.form.get('id')
    tour = Tour.query.get(tour_id)
    if tour is None:
        return jsonify({'code': 400, 'message': "no activity found"})
    tour.status = "deleted"
    db.session.commit()
    return redirect(url_for('manager.tours'))


@bp.route("/tours")
def tours():
    return render_template("tour.html")

@bp.route("/add_hotel")
def add_hotel():
    hotel = Hotel()
    hotel.status = "published"
    hotel.name = request.form.get("name")
    hotel.min_price = float(request.form.get("min_price"))
    hotel.room_num = int(request.form.get("room_num"))
    hotel.city = request.form.get("city")
    hotel.state = request.form.get("state")
    hotel.address = request.form.get("address")
    hotel.min_stay = request.form.get("min_stay")
    hotel.security = request.form.get("security")
    hotel.on_site_staff = request.form.get("on_site_stuff")
    hotel.house_keeping = request.form.get("house_keeping")
    hotel.front_desk = request.form.get("front_desk")
    hotel.bathroom = request.form.get("bathroom")
    hotel.room_type_num = request.form.get("room_type_num")
    hotel.description = request.form.get("description")
    images = request.files.getlist("images")
    max_id = db.session.query(db.func.max(Tour.id)).scalar()
    if max_id is None:
        max_id = 1
    else:
        max_id = max_id + 1
    img_routes = []
    folder_path = os.path.join(current_app.root_path, "static", "hotel_img", str(max_id))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for image in images:
        save_path = os.path.join(folder_path, image.filename)
        image.save(save_path)
        img_routes.append(save_path)
    hotel.images = json.dumps({"images": img_routes})
    hotel.total_star = 0
    hotel.review_num = 0
    hotel.star_detail = json.dumps({"star_detail": []})
    hotel.contact_name = request.form.get("contact_name")
    hotel.contact_email = request.form.get("contact_email")
    hotel.contact_phone = request.form.get("contact_phone")
    type_num = int(hotel.room_type_num)
    des = []
    i = 1
    while i <= type_num:
        sub_folder_path = os.path.join(folder_path, i)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        images = request.files.getlist(f"room_images_{i}")
        img_route = []
        for image in images:
            route = os.path.join(sub_folder_path, image.filename)
            image.save(route)
            img_route.append(route)
        des.append({"id": i,
                    "name": request.form.get(f"itinerary_name_{i}"),
                    "price": request.form.get(f"itinerary_desc_{i}"),
                    "picture": img_route})
        i = i + 1
    hotel.room_detail = json.dumps({"tour_des": des})
    amenities = []
    for i in range(1, 21):
        amenities[i] = request.form.get(f"aminity{i}")
    hotel.amenities = str(amenities)
    db.session.add(hotel)
    db.session.commit()
    return redirect(url_for("manager.tours"))

@bp.route("/accommodations")
def accommodations():
    return render_template("accommodation.html")

@bp.route("/flights")
def flights():
    return render_template("flight.html")
