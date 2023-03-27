from exts import db
from flask_login import UserMixin


class Customer(db.Model, UserMixin):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    nickname = db.Column(db.String(255))
    password = db.Column(db.String(255))
    avatarURL = db.Column(db.Text)
    wallet = db.Column(db.Float)
    orders = db.relationship('ActivityOrder', backref='customer')
    reviews = db.relationship('ActivityReview', backref='customer')


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    postTime = db.Column(db.DateTime)
    isRead = db.Column(db.Boolean)
    receiverID = db.Column(db.String(255))
    senderID = db.Column(db.String(255))


class ActivityOrder(db.Model):
    __tablename__ = 'activity_orders'

    id = db.Column(db.Integer, primary_key=True)
    startTime = db.Column(db.DateTime)
    endTime = db.Column(db.DateTime)
    cost = db.Column(db.Float)
    purchased = db.Column(db.Boolean)
    productID = db.Column(db.Integer, db.ForeignKey('activities.id'))
    customerID = db.Column(db.Integer, db.ForeignKey('customers.id'))


class ActivityReview(db.Model):
    __tablename__ = 'activity_reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    issueTime = db.Column(db.DateTime)
    content = db.Column(db.Text)
    customerID = db.Column(db.Integer, db.ForeignKey('customers.id'))
    productID = db.Column(db.Integer, db.ForeignKey('activities.id'))


class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    category = db.Column(db.String(255))
    status = db.Column(db.String(255))
    price = db.Column(db.Float)
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    address = db.Column(db.Text)
    duration = db.Column(db.Integer)
    group_size = db.Column(db.Integer)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    images = db.Column(db.Text)
    description = db.Column(db.Text)
    included = db.Column(db.Text)
    excluded = db.Column(db.Text)
    openHour = db.Column(db.DateTime)
    visitHour = db.Column(db.Integer)
    total_star = db.Column(db.Integer)
    review_num = db.Column(db.Integer)
    star_detail = db.Column(db.Text)
    contact_name = db.Column(db.String(255))
    contact_email = db.Column(db.String(255))
    contact_phone = db.Column(db.String(255))
    review = db.relationship('ActivityReview', backref='product')
    orders = db.relationship('ActivityOrder', backref='product')



