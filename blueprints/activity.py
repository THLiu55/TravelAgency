import json
import datetime

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from model import *
from exts import db
from utils.decorators import login_required
import re

bp = Blueprint("activity", __name__, url_prefix="/activity")


@bp.route('/add_review', methods=['POST'])
def add_review():
    activity_id = request.form.get('productId')
    customer_id = session.get('customer_id')
    rating = request.form.get('rating')
    content = request.form.get('content')
    # check if all the data have been entered
    if not customer_id or not rating or not content:
        return jsonify({'code': 400, 'message': 'Invalid data'})
    # check if activity exist
    activity = Activity.query.get(activity_id)
    if activity is None:
        return jsonify({'code': 400, 'message': 'Activity not found'})
    # check if the customer has ordered the activity
    # order = ActivityOrder.query.filter_by(customerID=customer_id, productID=activity_id).first()
    # if order is None:
    #     return jsonify({'code': 400, 'message': 'No order'})
    review = ActivityReview(rating=rating, issueTime=datetime.datetime.now(), content=content, customerID=customer_id,
                            productID=activity_id)
    activity.review_num = activity.review_num + 1
    db.session.add(review)
    db.session.commit()
    return redirect(url_for('activity.activityDetail', activity_id=activity.id))


@bp.route('/<page_num>', methods=['GET', 'POST'])
def activityList(page_num):
    logged = False if session.get('customer_id') is None else True
    total_activities = Activity.query.count()
    pagination = Activity.query.paginate(page=int(page_num), per_page=9, error_out=False)
    activities = pagination.items
    for activity in activities:
        # noinspection PyTypeChecker
        activity.images = json.loads(activity.images)['images']
        activity.images[0] = activity.images[0][activity.images[0].index('static'):].lstrip('static')
    return render_template('activity-grid.html', total_activities=total_activities, activities=activities,
                           page_num=page_num, logged=logged)


@bp.route('/details/<activity_id>/', methods=['GET', 'POST'])
def activityDetail(activity_id):
    activity = Activity.query.get(activity_id)
    reviews = activity.review
    activity.included = json.loads(activity.included)['included']
    activity.included = [i for i in activity.included if i is not None]
    activity.excluded = json.loads(activity.excluded)['not_included']
    activity.excluded = [i for i in activity.excluded if i is not None]
    activity.images = json.loads(activity.images)['images']
    images = [image[image.index('static'):].lstrip('static') for image in activity.images]
    for review in reviews:
        review.customerID = Customer.query.get(review.customerID).nickname
        review.issueTime = review.issueTime.strftime("%Y-%m-%d %H:%M")
    wishlist_exists = ActivityOrder.query.filter_by(customerID=session.get("customer_id"),
                                                    productID=activity_id, purchased=False).first()
    added = True if wishlist_exists is not None else False
    purchased = ActivityOrder.query.filter_by(customerID=session.get("customer_id"),
                                              productID=activity_id, purchased=True).first()
    logged = True if session.get("customer_id") and purchased else False
    activity.review_num = activity.review_num + 1
    db.session.commit()
    return render_template("activity-detail.html", activity=activity, logged=logged, reviews=reviews, images=images,
                           added=added)


@bp.route('/activity_filter', methods=['GET', 'POST'])
def activity_filter():
    activity_type = request.form.get("type1").split(",")
    to_sort = request.form.get('sort_by')
    if activity_type[0] == '':
        activity_type = ['Food & Nightlife', 'Hot Air Balloon', 'Mountain Climbing', 'Bike Ride']
    activity_price = request.form.get('activityPrice')
    activity_price = activity_price.split(',')
    min_price = int(activity_price[0])
    max_price = int(activity_price[-1])
    activity_duration = request.form.get('activityDuration').split(",")
    if activity_duration[0] == '':
        query = Activity.query.filter(Activity.category.in_(activity_type),
                                      Activity.price.between(min_price, max_price)
                                      )
    else:
        activity_duration = activity_duration[0].split('-')
        min_hour = int(activity_duration[0])
        max_hour = int(activity_duration[-1])
        query = Activity.query.filter(Activity.category.in_(activity_type),
                                      Activity.price.between(min_price, max_price),
                                      Activity.duration.between(min_hour, max_hour)
                                      )

    page = int(request.form.get('page'))
    pagination = query.paginate(page=page, per_page=9)
    activities = pagination.items
    for activity_i in activities:
        activity_i.contact_email = url_for('activity.activityDetail', activity_id=activity_i.id)
        activity_i.images = json.loads(activity_i.images)['images']
        activity_i.images[0] = "../" + activity_i.images[0][activity_i.images[0].index('static'):].replace('\\', '/')

    if to_sort == '2':
        activities = sorted(activities, key=lambda activity: activity.view_num, reverse=False)

    if to_sort == '3':
        activities = sorted(activities, key=lambda activity: activity.price, reverse=False)

    if to_sort == '4':
        activities = sorted(activities, key=lambda activity: activity.price, reverse=True)

    activities = [activity.to_dict() for activity in activities]
    return jsonify({"activities": activities, "page": 1})


@bp.route("/order-confirm", methods=['POST'])
def order_confirm():
    customer_id = session.get('customer_id')
    if customer_id:
        activity_id = request.form.get("activity_id")
        to_confirmed = Activity.query.get(activity_id)
        order_date = request.form.get("journey-date")
        customer = Customer.query.get(customer_id)
        return render_template("activity-booking-confirm.html", activity=to_confirmed, customer=customer,
                               order_date=order_date, logged=True)
    else:
        url = request.referrer
        return render_template("SignInUp.html", url=url)


@bp.route("/order-success")
def order_success():
    customer = Customer.query.get(session.get("customer_id"))
    cost = float(request.args.get("cost"))
    if customer.wallet >= cost:
        activity_order = ActivityOrder()
        activity_order.customerID = session.get('customer_id')
        activity_order.purchased = True
        activity_order.startTime = datetime.datetime.now()
        end_date = request.args.get("date")
        date_format = "%Y/%m/%d"
        datetime_obj = datetime.datetime.strptime(end_date, date_format)
        activity_order.endTime = datetime_obj
        activity_order.productID = request.args.get("activity_id")
        activity_order.cost = cost
        customer.wallet = customer.wallet - cost
        db.session.add(activity_order)
        db.session.commit()
        return render_template("booking-success.html", name=request.args.get("name"))
    else:
        return jsonify({"balance": 400})


@bp.route("/add_wishlist/<activity_id>")
def add_wishlist(activity_id):
    aimed_activity = Activity.query.get(activity_id)
    activity_order = ActivityOrder()
    activity_order.cost = aimed_activity.price
    activity_order.startTime = datetime.datetime.now()
    activity_order.purchased = False
    activity_order.customerID = session.get("customer_id")
    activity_order.productID = activity_id
    db.session.add(activity_order)
    db.session.commit()
    return redirect(url_for('customer.profile'))


@bp.route("/remove_wishlist/<activity_id>")
def remove_wishlist(activity_id):
    activity_order = ActivityOrder.query.filter_by(customerID=session.get("customer_id"), productID=activity_id,
                                                   purchased=False).first()
    db.session.delete(activity_order)
    db.session.commit()
    return redirect(url_for('customer.profile'))
