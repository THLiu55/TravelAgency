import json
import requests as req
from sqlalchemy import func
from datetime import datetime, timedelta

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


from utils.decorators import staff_login_required

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
bp = Blueprint("manager", __name__, url_prefix="/manager")


@bp.route("/")
@staff_login_required
def manager_homepage():
    db.create_all()
    today = datetime.now().date()
    one_day_ago = today - timedelta(days=1)

    today_reviews = (
        db.session.query(func.count(ActivityReview.id))
        .filter(
            ActivityReview.issueTime >= today,
            ActivityReview.issueTime < today + timedelta(days=1),
        )
        .scalar()
        or 0
    )
    today_reviews += (
        db.session.query(func.count(TourReview.id))
        .filter(
            TourReview.issueTime >= today,
            TourReview.issueTime < today + timedelta(days=1),
        )
        .scalar()
        or 0
    )
    today_reviews += (
        db.session.query(func.count(HotelReview.id))
        .filter(
            HotelReview.issueTime >= today,
            HotelReview.issueTime < today + timedelta(days=1),
        )
        .scalar()
        or 0
    )

    today_customers = (
        db.session.query(func.count())
        .filter(
            Customer.join_date >= today, Customer.join_date < today + timedelta(days=1)
        )
        .scalar()
        or 0
    )

    today_orders = (
        db.session.query(func.count(ActivityOrder.id))
        .filter(
            ActivityOrder.startTime >= today,
            ActivityOrder.startTime < today + timedelta(days=1),
        )
        .scalar()
        or 0
    )
    today_orders += (
        db.session.query(func.count(TourOrder.id))
        .filter(
            TourOrder.startTime >= today,
            TourOrder.startTime < today + timedelta(days=1),
        )
        .scalar()
        or 0
    )
    today_orders += (
        db.session.query(func.count(HotelOrder.id))
        .filter(
            HotelOrder.endTime >= today, HotelOrder.endTime < today + timedelta(days=1)
        )
        .scalar()
        or 0
    )
    today_orders += (
        db.session.query(func.count(FlightOrder.id))
        .filter(
            FlightOrder.startTime >= today,
            FlightOrder.startTime < today + timedelta(days=1),
        )
        .scalar()
        or 0
    )

    total_reviews = (
        db.session.query(
            func.coalesce(func.sum(Activity.review_num), 0)
            + func.coalesce(func.sum(Tour.review_num), 0)
            + func.coalesce(func.sum(Hotel.review_num), 0)
        ).scalar()
        or 0
    )

    total_orders = (
        (db.session.query(func.count(TourOrder.id)).scalar() or 0)
        + (db.session.query(func.count(HotelOrder.id)).scalar() or 0)
        + (db.session.query(func.count(ActivityOrder.id)).scalar() or 0)
        + (db.session.query(func.count(FlightOrder.id)).scalar() or 0)
    )

    num_customers = db.session.query(func.count(Customer.id)).scalar() or 0

    print(today_orders)

    def get_percent(a, b):
        return 0 if b == 0 else int(100 * (a / b))

    upper_data = {
        "order_today": today_orders,
        "customer_today": today_customers,
        "reviews_today": today_reviews,
        "order_percent": get_percent(today_orders, total_orders),
        "customer_percent": get_percent(today_customers, num_customers),
        "reviews_percent": get_percent(today_reviews, total_reviews),
    }

    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    prev_date = start_date - timedelta(days=7)

    results = []
    profit_split = [0, 0, 0, 0]  # activity, tour, hotel, flight
    for order, i in zip([ActivityOrder, HotelOrder, TourOrder, FlightOrder], range(4)):
        tmp = (
            db.session.query(func.date(order.startTime), func.sum(order.cost))
            .filter(
                order.startTime <= end_date,
                order.startTime >= start_date,
                order.purchased == 1,
            )
            .group_by(func.date(order.startTime))
            .all()
        )
        profit_split[i] = sum([item[1] for item in tmp])
        results += tmp

    for order in [ActivityOrder, HotelOrder, TourOrder, FlightOrder]:
        results += (
            db.session.query(func.date(order.startTime), func.sum(order.cost))
            .filter(
                order.startTime <= start_date,
                order.startTime >= prev_date,
                order.purchased == 1,
            )
            .group_by(func.date(order.startTime))
            .all()
        )

    print(results)
    sum_profit = sum(profit_split)
    percent = (
        [25, 25, 25, 25]
        if sum_profit == 0
        else [int((i / sum_profit) * 100) for i in profit_split]
    )
    costs_dict = {}
    for i in range(14):
        date = end_date - timedelta(days=i)
        flag = True
        for result in results:
            if str(result[0]) == str(date.date()):
                costs_dict[date.date()] = (
                    result[1]
                    if date.date() not in costs_dict
                    else costs_dict[date.date()] + result[1]
                )
                flag = False
        if flag:
            costs_dict[date.date()] = 0

    ordered_values = [
        [costs_dict[k] for k in sorted(costs_dict.keys())][0:7],
        [costs_dict[k] for k in sorted(costs_dict.keys())][7:],
    ]
    print(ordered_values)
    data = {
        "profit_list": ordered_values,
        "profit_this": sum(ordered_values[1]),
        "profit_prev": sum(ordered_values[0]),
        "profit_split": profit_split,
        "percent": percent,
    }
    return render_template("Dashboard.html", upper_data=upper_data, data=data)


@bp.route("/logout")
def logout():
    return render_template("Stafflogin.html")


# @bp.route('/destination', methods=["POST"])
# def destinationList():
#     return render_template("destinations.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    url = request.args.get("url")
    print(f"here{url}")
    if request.method == "GET":
        return render_template("Stafflogin.html", url=url)
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["staff_id"] = 1
            return redirect(url_for("manager.manager_homepage"))
        return redirect(url_for("customer.homepage"))


@bp.route("/load_activities", methods=["POST"])
@staff_login_required
def load_activities():
    return load_product("Activity")


@bp.route("/add_activity", methods=["POST"])
@staff_login_required
def add_activity():
    activity = Activity()
    activity.status = "published"
    activity.name = request.form.get("name")
    activity.category = request.form.get("category")
    activity.price = float(request.form.get("price"))
    activity.city = request.form.get("city")
    activity.state = request.form.get("state")
    activity.address = request.form.get("address")
    address = activity.address + " " + activity.city + " " + activity.state
    url = "https://nominatim.openstreetmap.org/search?q={}&format=json".format(address)
    response = req.get(url).json()
    if len(response) > 0:
        activity.lat = response[0]["lat"]
        activity.lon = response[0]["lon"]
    else:
        return jsonify({"code": "invalid address "})
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
    activity.star_detail = json.dumps({"star_detail": [0, 0, 0, 0, 0]})
    activity.contact_name = request.form.get("contact_name")
    activity.contact_email = request.form.get("contact_email")
    activity.contact_phone = request.form.get("contact_phone")
    db.session.add(activity)
    db.session.commit()
    return redirect(url_for("manager.activities"))


@bp.route("/delete_activity", methods=["GET", "POST"])
@staff_login_required
def delete_activity():
    activity_id = request.form.get("id")
    activity = Activity.query.get(activity_id)
    if activity is None:
        return jsonify({"code": 400, "message": "no activity found"})
    activity.status = "deleted"
    db.session.commit()
    return redirect(url_for("manager.activities"))


@bp.route("/activities", methods=["GET", "POST"])
@staff_login_required
def activities():
    return render_template("activities.html")


### CHAT RELATED ###
@bp.route("/responding/<target_customer_id>/", methods=["GET", "POST"])
@staff_login_required
def respond_view(target_customer_id):
    """manager bargaining with target customer

    Args:
        targetcustomer_id (_type_): _description_

    Returns:
        _type_: _description_
    """

    target_customer = Customer.query.filter_by(id=target_customer_id).first()
    if target_customer:
        # TODO: load previous chat history from target_customer.messages
        return render_template("chat.html", target_customer=target_customer)
    else:
        return False


@bp.route("/chat_test", methods=["GET", "POST"])
def respond_test():
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
    return render_template("Test.html")


### END CHAT RELATED ###


@bp.route("/add_tour", methods=["GET", "POST"])
@staff_login_required
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
    tour.star_detail = json.dumps({"star_detail": [0, 0, 0, 0, 0]})
    tour.contact_name = request.form.get("contact_name")
    tour.contact_email = request.form.get("contact_email")
    tour.contact_phone = request.form.get("contact_phone")
    days = int(tour.duration)
    des = []
    i = 1
    while i <= days:
        des.append(
            {
                request.form.get(
                    "itinerary_name_{day}".format(day=i)
                ): request.form.get("itinerary_desc_{day}".format(day=i))
            }
        )
        i = i + 1
    tour.itineraries = json.dumps({"tour_des": des})
    db.session.add(tour)
    db.session.commit()
    return redirect(url_for("manager.tours"))


@bp.route("/load_tours", methods=["POST"])
@staff_login_required
def load_tours():
    return load_product("Tour")


@bp.route("/delete_tour", methods=["GET", "POST"])
@staff_login_required
def delete_tour():
    tour_id = request.form.get("id")
    tour = Tour.query.get(tour_id)
    if tour is None:
        return jsonify({"code": 400, "message": "no activity found"})
    tour.status = "deleted"
    db.session.commit()
    return redirect(url_for("manager.tours"))


@bp.route("/tours")
@staff_login_required
def tours():
    return render_template("tour.html")


@bp.route("/add_hotel", methods=["POST"])
@staff_login_required
def add_hotel():
    hotel = Hotel()
    hotel.status = "published"
    hotel.name = request.form.get("name")
    hotel.min_price = float(request.form.get("min_price"))
    hotel.room_num = int(request.form.get("room_num"))
    hotel.city = request.form.get("city")
    hotel.state = request.form.get("state")
    hotel.address = request.form.get("address")
    # address = hotel.address + " " + hotel.city + " " + hotel.state
    # url = 'https://nominatim.openstreetmap.org/search?q={}&format=json'.format(address)
    # response = req.get(url).json()
    # if len(response) > 0:
    #     hotel.lat = response[0]['lat']
    #     hotel.lon = response[0]['lon']
    # else:
    #     return jsonify({"code": "invalid address "})
    hotel.min_stay = request.form.get("min_stay")
    hotel.security = request.form.get("security")
    hotel.on_site_staff = request.form.get("on_site_staff")
    hotel.house_keeping = request.form.get("house_keeping")
    hotel.front_desk = request.form.get("front_desk")
    hotel.bathroom = request.form.get("bathroom")
    hotel.room_type_num = request.form.get("typenum")
    hotel.description = request.form.get("description")
    hotel.view_num = 0
    hotel.star = request.form.get("hotel_star")
    images = request.files.getlist("images")
    max_id = db.session.query(db.func.max(Hotel.id)).scalar()
    if max_id is None:
        max_id = 1
    else:
        max_id = max_id + 1
    img_routes = []
    folder_path = os.path.join(
        current_app.root_path, "static", "hotel_img", str(max_id)
    )
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for image in images:
        save_path = os.path.join(folder_path, image.filename)
        image.save(save_path)
        img_routes.append(save_path)
    hotel.images = json.dumps({"images": img_routes})
    hotel.total_star = 0
    hotel.review_num = 0
    hotel.star_detail = json.dumps({"star_detail": [0, 0, 0, 0, 0]})
    hotel.contact_name = request.form.get("contact_name")
    hotel.contact_email = request.form.get("contact_email")
    hotel.contact_phone = request.form.get("contact_phone")
    type_num = int(hotel.room_type_num)
    des = []
    i = 1
    while i <= type_num:
        sub_folder_path = os.path.join(folder_path, str(i))
        if not os.path.exists(sub_folder_path):
            os.makedirs(sub_folder_path)
        image = request.files.get(f"fileInput{i}")
        route = os.path.join(sub_folder_path, image.filename)
        image.save(route)
        features = []
        for j in range(1, 8):
            if request.form.get(f"feature_{j}_{i}") is not None:
                features.append(request.form.get(f"feature_{j}_{i}"))
        des.append(
            {
                "id": i,
                "name": request.form.get(f"hotelroom_name_{i}"),
                "features": features,
                "price": request.form.get(f"hotelroom_price_{i}"),
                "picture": route,
            }
        )
        i = i + 1
    hotel.room_detail = json.dumps({"hotel_des": des})
    amenities = []
    for i in range(1, 21):
        amin = request.form.get(f"aminity{i}")
        if amin is not None:
            amenities.append(amin)
    hotel.amenities = str(amenities)
    db.session.add(hotel)
    db.session.commit()
    return redirect(url_for("manager.accommodations"))


@bp.route("/load_hotels", methods=["POST"])
@staff_login_required
def load_hotels():
    return load_product("Hotel")


@bp.route("/delete_hotel", methods=["POST"])
@staff_login_required
def delete_hotel():
    hotel_id = request.form.get("id")
    hotel = Hotel.query.get(hotel_id)
    if hotel is None:
        return jsonify({"code": 400, "message": "no activity found"})
    hotel.status = "deleted"
    db.session.commit()
    return redirect(url_for("manager.accommodations"))


def load_product(product_name):
    product = (
        Hotel
        if product_name == "Hotel"
        else Tour
        if product_name == "Tour"
        else Activity
        if product_name == "Activity"
        else Flight
    )
    category = request.form.get("category")
    status = request.form.get("publish")
    q = product.query
    if product != Hotel and product != Flight and category != "All Category":
        q = q.filter_by(category=category)
    if status != "All Status":
        q = q.filter_by(status=status)
    products = [p.serialize() for p in q.all()]
    return jsonify({"code": 200, "content": products})


@bp.route("/accommodations")
@staff_login_required
def accommodations():
    return render_template("accommodation.html")


@bp.route("/add_flight", methods=["POST"])
@staff_login_required
def add_flight():
    # db.drop_all()
    # db.create_all()
    flight = Flight()
    flight.status = "published"
    flight.departure = request.form.get("departure")
    flight.destination = request.form.get("destination")
    flight.flight_type = request.form.get("flight_type")
    flight.takeoff_time = datetime.strptime(
        request.form.get("take_off_time"), "%H:%M"
    ).time()
    flight.landing_time = datetime.strptime(
        request.form.get("landing_time"), "%H:%M"
    ).time()
    flight.week_day = request.form.get("day_of_week")
    flight.flight_stop = request.form.get("flight_stop")
    flight.company = request.form.get("company")
    print(request.form.get("total_time"))
    flight.total_time = float(request.form.get("total_time"))
    flight.price = float(request.form.get("price"))
    flight.fare_type = request.form.get("fare_type")
    flight.flight_class = request.form.get("flight_class")
    flight.cancellation_charge = request.form.get("cancellation_charge")
    flight.flight_charge = request.form.get("flight_charge")
    flight.seat_baggage = request.form.get("seat_baggage")
    flight.base_fare = request.form.get("base_fare")
    flight.taxes = request.form.get("taxes")
    images = request.files.getlist("images")
    max_id = db.session.query(db.func.max(Flight.id)).scalar()
    max_id = 1 if max_id is None else max_id + 1
    img_routes = []
    folder_path = os.path.join(
        current_app.root_path, "static", "flight_img", str(max_id)
    )
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for image in images:
        save_path = os.path.join(folder_path, image.filename)
        image.save(save_path)
        img_routes.append(save_path)
    flight.images = json.dumps({"images": img_routes})
    flight.description = request.form.get("description")
    inflight_features = []
    for i in range(1, 13):
        amin = request.form.get(f"inflight{i}")
        if amin is not None:
            inflight_features.append(amin)
    flight.inflight_features = str(inflight_features)
    flight.total_star = 0
    flight.review_num = 0
    flight.star_detail = json.dumps({"star_detail": [0, 0, 0, 0, 0]})
    flight.contact_name = request.form.get("contact_name")
    flight.contact_email = request.form.get("contact_email")
    flight.contact_phone = request.form.get("contact_phone")
    flight.view_num = 0
    db.session.add(flight)
    db.session.commit()
    return redirect(url_for("manager.flights"))


@bp.route("/load_flights", methods=["POST"])
@staff_login_required
def load_flights():
    return load_product("Flight")


@bp.route("/delete_flight", methods=["POST"])
@staff_login_required
def delete_flight():
    flight_id = request.form.get("id")
    flight = Flight.query.get(flight_id)
    print("here")
    if flight is None:
        return jsonify({"code": 400, "message": "no activity found"})
    flight.status = "deleted"
    db.session.commit()
    return redirect(url_for("manager.flights"))


@bp.route("/flights")
@staff_login_required
def flights():
    return render_template("flight.html")


@bp.route("/customers")
@staff_login_required
def customers():
    return render_template("customerAccount.html")


@bp.route("/wish_list")
@staff_login_required
def wish_list():
    return render_template("customerWishlist.html")


@bp.route("/chat")
@staff_login_required
def chat():
    return render_template("chat.html")


# previous order_details
@bp.route("/activity_invoice")
@staff_login_required
def activity_invoice():
    return render_template("orderInvoiceActivity.html")


@bp.route("/hotel_invoice")
@staff_login_required
def hotel_invoice():
    return render_template("orderInvoiceHotel.html")


@bp.route("/tour_invoice")
@staff_login_required
def tour_invoice():
    return render_template("orderInvoiceTour.html")


@bp.route("/flight_invoice")
@staff_login_required
def flight_invoice():
    return render_template("orderInvoiceFlight.html")


@bp.route("/order_history")
@staff_login_required
def order_history():
    return render_template("orderHistory.html")


@bp.route("/order_status")
@staff_login_required
def order_status():
    return render_template("orderStatus.html")


@bp.route("/order_message")
@staff_login_required
def order_messages():
    return render_template("orderMessages.html")


@bp.route("/reviews")
@staff_login_required
def reviews():
    return render_template("reviews.html")


@bp.route("/total_orders")
@staff_login_required
def total_orders():
    return render_template("orders.html")


@bp.route("/load_graph", methods=["POST"])
@staff_login_required
def load_graph():
    today = datetime.today()
    start_date = today - timedelta(days=6)
    date_strings = []
    while start_date <= today:
        date_strings.append(start_date.strftime("%d %b"))
        start_date += timedelta(days=1)

    graph_data = {"x_axis": date_strings}
    return jsonify({"code": 200, "data": graph_data})


@bp.route("/load_orders", methods=["POST", "GET"])
@staff_login_required
def load_orders():
    category = request.form.get("category")
    orders = []
    if category == "all":
        orders += [
            order.serialize()
            for order in TourOrder.query.filter_by(purchased=True).all()
        ]
        orders += [
            order.serialize()
            for order in ActivityOrder.query.filter_by(purchased=True).all()
        ]
        orders += [
            order.serialize()
            for order in HotelOrder.query.filter_by(purchased=True).all()
        ]
        orders += [
            order.serialize()
            for order in FlightOrder.query.filter_by(purchased=True).all()
        ]
    else:
        order_data = (
            TourOrder
            if category == "tour"
            else ActivityOrder
            if category == "activity"
            else HotelOrder
            if category == "hotel"
            else FlightOrder
        )
        orders += [order.serialize() for order in order_data.query.all()]
    db.session.commit()
    return jsonify({"code": 200, "content": orders})


@bp.route("/load_reviews", methods=["POST", "GET"])
@staff_login_required
def load_reviews():
    review_list = []
    review_list += [review.serialize() for review in ActivityReview.query.all()]
    review_list += [review.serialize() for review in HotelReview.query.all()]
    review_list += [review.serialize() for review in TourReview.query.all()]
    db.session.commit()
    return jsonify({"code": 200, "content": review_list})
