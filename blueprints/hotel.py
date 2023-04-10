import json, math

from flask import Blueprint, render_template, request, jsonify, current_app, session, redirect, url_for
from model import *
from exts import db
from sqlalchemy import or_

bp = Blueprint("hotel", __name__, url_prefix="/hotel")


@bp.route("/<page_num>")
def hotelList(page_num):
    logged = False if session.get('customer_id') is None else True
    total_hotels = Hotel.query.count()
    pagination = Hotel.query.paginate(page=int(page_num), per_page=9, error_out=False)
    hotels = pagination.items
    for single_hotel in hotels:
        # noinspection PyTypeChecker
        single_hotel.images = json.loads(single_hotel.images)['images']
        single_hotel.images[0] = single_hotel.images[0][single_hotel.images[0].index('static'):].lstrip('static')
    return render_template("hotel-grid.html", total_hotels=total_hotels, hotels=hotels, logged=logged,
                           page_num=page_num)


@bp.route("/hotel_filter", methods=['POST', 'GET'])
def hotel_filter():
    hotel_type = request.form.get("type1").split(",")
    to_sort = request.form.get('sort_by')
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
    pagination = query.paginate(page=page, per_page=9)
    hotels = pagination.items
    for hotel_i in hotels:
        hotel_i.contact_email = url_for('hotel.hotelDetail', hotel_id=hotel_i.id)
        hotel_i.images = json.loads(hotel_i.images)['images']
        hotel_i.images[0] = "../" + hotel_i.images[0][hotel_i.images[0].index('static'):].replace('\\', '/')

    if to_sort == '2':
        hotels = sorted(hotels, key=lambda hotel: hotel.view_num, reverse=False)

    if to_sort == '3':
        hotels = sorted(hotels, key=lambda hotel: hotel.min_price, reverse=False)

    if to_sort == '4':
        hotels = sorted(hotels, key=lambda hotel: hotel.min_price, reverse=True)
    hotels = [hotel.to_dict() for hotel in hotels]
    return jsonify({"hotels": hotels, "page": 1})


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
    for room in rooms:
        room['picture'] = room['picture'][room['picture'].index('static'):].lstrip('static')
    return render_template("hotel-detail.html", hotel=hotel, logged=logged, reviews=reviews, images=images,
                           review_num=review_num, added=added, purchased=purchased, star_score=star_score,
                           star_score_ceil=star_score_ceil, star_detail=star_detail, rooms=rooms)
