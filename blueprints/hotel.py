import json, math
from datetime import timedelta, date, datetime

from flask import Blueprint, render_template, request, jsonify, current_app, session, redirect, url_for, flash
from model import *
from exts import db
from sqlalchemy import or_
from translations.translator import translator

bp = Blueprint("hotel", __name__, url_prefix="/hotel")


@bp.route("/<page_num>")
def hotelList(page_num):
    logged = False if session.get('customer_id') is None else True
    total_hotels = Hotel.query.count()
    pagination = Hotel.query.filter_by(status="published").paginate(page=int(page_num), per_page=18, error_out=False)
    hotels = pagination.items
    for single_hotel in hotels:
        # noinspection PyTypeChecker
        single_hotel.images = json.loads(single_hotel.images)['images']
        single_hotel.images[0] = single_hotel.images[0][single_hotel.images[0].index('static'):].lstrip('static')
        star_detail = json.loads(single_hotel.star_detail)['star_detail']
        single_hotel.score = round(sum(star_detail) / single_hotel.review_num, 1) if single_hotel.review_num != 0 else 0
        if single_hotel.review_num == 0:
            single_hotel.score = 3.0
            single_hotel.tag = 'Nice'
        else:
            if single_hotel.score >= 4:
                single_hotel.tag = 'Excellent'
            elif single_hotel.score >= 3:
                single_hotel.tag = 'Nice'
            else:
                single_hotel.tag = 'Good'
    hotels = sorted(hotels, key=lambda hotel: hotel.priority, reverse=True)
    result = request.args.get('result')
    return render_template("hotel-grid.html", total_hotels=total_hotels, hotels=hotels, logged=logged,
                           page_num=page_num, result=result)


@bp.route("/hotel_filter", methods=['POST', 'GET'])
def hotel_filter():
    hotel_type = request.form.get("type1").split(",")
    to_sort = request.form.get('sort_by')
    if 'language' in session:
        if session.get("language") == 'zh':
            key_word = request.form.get('key-word')
            key_word = translator(key_word, 'zh', 'en')
        else:
            key_word = request.form.get('key-word')
    else:
        key_word = request.form.get('key-word')
    if hotel_type[0] == '':
        hotel_type = ['Free Parking', 'Restaurant', 'Pets Allowed', 'Airport Transportation', 'Fitness Facility',
                      'WiFi', 'Air Conditioning']
    hotel_price = request.form.get('activityPrice')
    hotel_price = hotel_price.split(',')
    mi_price = int(hotel_price[0])
    max_price = int(hotel_price[-1])
    hotel_star = request.form.get('hotel_star').split(",")
    if hotel_star[0] == '':
        hotel_star = ['1', '2', '3', '4', '5']
    query = Hotel.query.filter(Hotel.min_price.between(mi_price, max_price), Hotel.star.in_(hotel_star),
                               or_(*[Hotel.amenities.like(f'%{word}%') for word in hotel_type]))
    page = int(request.form.get('page'))
    pagination = query.paginate(page=page, per_page=18)
    hotels = pagination.items
    for hotel_i in hotels:
        hotel_i.contact_email = url_for('hotel.hotelDetail', hotel_id=hotel_i.id)
        hotel_i.images = json.loads(hotel_i.images)['images']
        hotel_i.images[0] = "../" + hotel_i.images[0][hotel_i.images[0].index('static'):].replace('\\', '/')
    if to_sort == '1':
        hotels = sorted(hotels, key=lambda hotel: hotel.priority, reverse=True)

    if to_sort == '2':
        hotels = sorted(hotels, key=lambda hotel: hotel.view_num, reverse=True)

    if to_sort == '3':
        hotels = sorted(hotels, key=lambda hotel: hotel.min_price, reverse=False)

    if to_sort == '4':
        hotels = sorted(hotels, key=lambda hotel: hotel.min_price, reverse=True)
    for activity in hotels:
        star_detail = json.loads(activity.star_detail)['star_detail']
        activity.contact_phone = round(sum(star_detail) / activity.review_num, 1) if activity.review_num != 0 else 0
        if activity.review_num == 0:
            activity.contact_phone = '3.0'
            activity.lat = 'Nice'
        else:
            if activity.contact_phone >= 4:
                activity.lat = 'Excellent'
            elif activity.contact_phone >= 3:
                activity.lat = 'Nice'
            else:
                activity.lat = 'Good'
    hotels = [hotel.to_dict() for hotel in hotels]
    return jsonify({"hotels": hotels, "page": 1, "keyword": key_word})


@bp.route('/details/<hotel_id>/', methods=['GET', 'POST'])
def hotelDetail(hotel_id):
    hotel = Hotel.query.get(hotel_id)
    hotel.view_num = hotel.view_num + 1
    db.session.commit()
    reviews = hotel.review
    hotel.images = json.loads(hotel.images)['images']
    images = [image[image.index('static'):].lstrip('static') for image in hotel.images]
    for review in reviews:
        review.customerID = Customer.query.get(review.customerID).nickname
        review.issueTime = review.issueTime.strftime("%Y-%m-%d %H:%M")
    wishlist_exists = HotelOrder.query.filter_by(customerID=session.get("customer_id"),
                                                 productID=hotel.id, purchased=False).first()
    added = True if wishlist_exists is not None else False
    purchased = HotelOrder.query.filter_by(customerID=session.get("customer_id"),
                                           productID=hotel_id, purchased=True).first()
    logged = session.get("customer_id")
    purchased = True if (purchased is not None and logged is not None) else False
    logged = True if logged else False
    star_detail = json.loads(hotel.star_detail)['star_detail']
    star_score = round(sum(star_detail) / hotel.review_num, 1) if hotel.review_num != 0 else 0
    star_score_ceil = math.floor(star_score)
    review_num = hotel.review_num
    hotel.review_num = 10000 if hotel.review_num == 0 else hotel.review_num
    rooms = json.loads(hotel.room_detail)['hotel_des']
    rooms_dic = []
    for room_i in rooms:
        room = Room()
        room.id = room_i["id"]
        room.picture = room_i['picture'][room_i['picture'].index('static'):].lstrip('static')
        room.wifi = True if "WiFi" in room_i['features'] else False
        room.square_1 = True if "15 ㎡" in room_i['features'] else False
        room.square_2 = True if "25 ㎡" in room_i['features'] else False
        room.bed_1 = True if "1 Single bed" in room_i['features'] else False
        room.bed_2 = True if "2 single beds" in room_i['features'] else False
        room.free = True if "Free Toiletries" in room_i['features'] else False
        room.shower = True if "Shower And Bathtub" in room_i['features'] else False
        room.price = float(room_i['price'])
        rooms_dic.append(room)
    wine_bar = True if "Wine Bar" in hotel.amenities else False
    free_parking = True if "Free Parking" in hotel.amenities else False
    doorman = True if "Doorman" in hotel.amenities else False
    suitable = True if "Suitable For Events" in hotel.amenities else False
    pets_allowed = True if "Pets Allowed" in hotel.amenities else False
    handicap = True if "Handicap Accessible" in hotel.amenities else False
    breakfast = True if "Breakfast" in hotel.amenities else False
    fitness_facility = True if "Fitness Facility" in hotel.amenities else False
    elevator = True if "Elevator In Building" in hotel.amenities else False
    entertainment = True if "Entertainment" in hotel.amenities else False
    air_conditioning = True if "Air Conditioning" in hotel.amenities else False
    coffee = True if "Coffee" in hotel.amenities else False
    wifi = True if "WiFi" in hotel.amenities else False
    swimming_pool = True if "Swimming Pool" in hotel.amenities else False
    play = True if "Beverage Selection" in hotel.amenities else False
    pick_and_drop = True if "Airport Transportation" in hotel.amenities else False
    fridge = True if "Bar / Lounge" in hotel.amenities else False
    if hotel.min_stay == "More Than 2 Nights":
        min_stay = "More Than 2 Nights"
        hotel.min_stay = True
    else:
        min_stay = "2 Nights Or Less"
        hotel.min_stay = False
    available_days = []
    start_date = date.today()
    end_date = start_date + timedelta(days=3 * 30)
    while start_date <= end_date:
        available_days.append(start_date.strftime("%Y-%m-%d") + ',')
        start_date += timedelta(days=1)
    return render_template("hotel-detail.html", hotel=hotel, logged=logged, reviews=reviews, images=images,
                           review_num=review_num, added=added, purchased=purchased, star_score=star_score,
                           star_score_ceil=star_score_ceil, star_detail=star_detail, rooms=rooms_dic, wine_bar=wine_bar,
                           doorman=doorman, suitable=suitable, free_parking=free_parking, pets_allowed=pets_allowed,
                           handicap=handicap, television=True, fridge=fridge, secure=True, pick_and_drop=pick_and_drop,
                           room_service=True, fire_place=True, breakfast=breakfast, fitness_facility=fitness_facility,
                           elevator=elevator, entertainment=entertainment, air_conditioning=air_conditioning,
                           coffee=coffee, wifi=wifi, swimming_pool=swimming_pool, play=play, room_num=len(rooms),
                           min_stay=min_stay, lat=hotel.lat, lon=hotel.lon, available_days=''.join(available_days))


@bp.route("/add_wishlist/<hotel_id>")
def add_wishlist(hotel_id):
    aimed_hotel = Hotel.query.get(hotel_id)
    hotel_order = HotelOrder()
    hotel_order.customerID = session.get("customer_id")
    hotel_order.productID = hotel_id
    hotel_order.cost = aimed_hotel.min_price
    hotel_order.purchased = False
    hotel_order.endTime = datetime.now()
    db.session.add(hotel_order)
    db.session.commit()
    return redirect((url_for('customer.profile', page="/wishlist")))


@bp.route("/remove_wishlist/<hotel_id>")
def remove_wishlist(hotel_id):
    hotel_order = HotelOrder.query.filter_by(customerID=session.get("customer_id"), productID=hotel_id,
                                             purchased=False).first()
    db.session.delete(hotel_order)
    db.session.commit()
    return redirect(url_for('customer.profile', page="/wishlist"))


@bp.route("/order-confirm", methods=['POST'])
def order_confirm():
    customer_id = session.get('customer_id')
    if customer_id:
        customer = Customer.query.get(customer_id)
        hotel_id = request.form.get("hotel_id")
        hotel = Hotel.query.get(hotel_id)
        to_confirmed = Hotel.query.get(hotel_id)
        hotel_order = HotelOrder()
        hotel_order.customerID = customer_id
        hotel_order.productID = hotel_id
        hotel_order.purchased = False
        hotel_order.cost = float(request.form.get("price-total"))
        hotel_order.startTime = request.form.get("journey-date")
        hotel_order.checkOutTime = request.form.get("return-date")
        hotel_order.roomID = request.form.get("room_id")
        rooms = json.loads(hotel.room_detail)['hotel_des']
        room_name = ""
        room_id = ""
        for room_i in rooms:
            if str(room_i["id"]) == hotel_order.roomID:
                room_name = room_i["name"]
                room_id = room_i["id"]
                break
        return render_template("hotel-booking-confirm.html", hotel=to_confirmed, customer=customer,
                               hotel_order=hotel_order, logged=True, room_name=room_name, room_id=room_id)
    else:
        url = request.referrer
        return render_template("SignInUp.html", url=url)


@bp.route("/order-success")
def order_success():
    customer = Customer.query.get(session.get("customer_id"))
    cost = float(request.args.get("cost"))
    if customer.wallet >= cost:
        hotel_order = HotelOrder()
        hotel_order.customerID = session.get('customer_id')
        hotel_order.purchased = True
        hotel_order.roomID = request.args.get("roomID")
        s_date = request.args.get("s_date")
        e_date = request.args.get("e_date")
        try:
            date_format = "%Y/%m/%d"
            datetime_s = datetime.strptime(s_date, date_format)
        except ValueError:
            date_format = "%m/%d/%Y"
            datetime_s = datetime.strptime(s_date, date_format)
        try:
            date_format = "%Y/%m/%d"
            datetime_e = datetime.strptime(e_date, date_format)
        except ValueError:
            date_format = "%m/%d/%Y"
            datetime_e = datetime.strptime(e_date, date_format)
        hotel_order.startTime = datetime_s
        hotel_order.productID = request.args.get("hotel_id")
        hotel_order.cost = float(request.args.get("cost"))
        hotel_order.checkOutTime = datetime_e
        hotel_order.endTime = datetime.now()
        customer.wallet = customer.wallet - cost
        one_hour_ago = datetime.now() - timedelta(hours=1)
        last_order = HotelOrder.query.filter_by(customerID=customer.id, productID=hotel_order.productID).filter(
            HotelOrder.endTime <= one_hour_ago).all()
        db.session.add(hotel_order)
        db.session.commit()
        return render_template("booking-success.html", name=request.args.get("name"), logged=True)
    else:
        return redirect(url_for('customer.wallet_re_jump', id=request.args.get("hotel_id"), type="hotel"))


@bp.route("/add_review", methods=['POST'])
def add_review():
    hotel_id = request.form.get('productId')
    customer_id = session.get('customer_id')
    rating = request.form.get('rating')
    content = request.form.get('content')
    hotel = Hotel.query.get(hotel_id)
    review = HotelReview(rating=rating, issueTime=datetime.now(), content=content, customerID=customer_id,
                         productID=hotel_id)
    hotel.review_num = hotel.review_num + 1
    star = int(request.form.get("rating"))
    star_index = star - 1
    star_detail = json.loads(hotel.star_detail)["star_detail"]
    star_detail[star_index] = star_detail[star_index] + star
    hotel.star_detail = json.dumps({"star_detail": star_detail})
    db.session.add(review)
    db.session.commit()
    return redirect(url_for('hotel.hotelDetail', hotel_id=hotel_id))
