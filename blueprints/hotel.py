import json, math

from flask import Blueprint, render_template, request, jsonify, current_app, session, redirect, url_for
from model import *
from exts import db

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
    return render_template("hotel-grid.html", total_hotels=total_hotels, hotels=hotels, logged=logged)


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
