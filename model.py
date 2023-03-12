from exts import db
from flask_login import UserMixin


class Customer(db.Model, UserMixin):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    nickname = db.Column(db.String(255))
    password = db.Column(db.String(255))
    avatarURL = db.Column(db.String(255))
    wallet = db.Column(db.Float)
    orders = db.relationship('Order', backref='customer')
    reviews = db.relationship('Review', backref='customer')


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    postTime = db.Column(db.DateTime)
    isRead = db.Column(db.Boolean)
    receiverID = db.Column(db.String(255))
    senderID = db.Column(db.String(255))


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    startTime = db.Column(db.DateTime)
    endTime = db.Column(db.DateTime)
    cost = db.Column(db.Float)
    type = db.Column(db.String(255))
    productID = db.Column(db.Integer, db.ForeignKey('products.id'))
    customerID = db.Column(db.Integer, db.ForeignKey('customers.id'))


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    issueTime = db.Column(db.DateTime)
    content = db.Column(db.Text)
    customerID = db.Column(db.Integer, db.ForeignKey('customers.id'))
    productID = db.Column(db.Integer, db.ForeignKey('products.id'))


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    address = db.Column(db.String(255))
    coverURL = db.Column(db.String(255))
    description = db.Column(db.Text)
    extraInfo = db.Column(db.Text)
    reviewedNum = db.Column(db.Integer)
    totalStars = db.Column(db.Integer)
    price = db.Column(db.Float)
    type = db.Column(db.String(255))
    orders = db.relationship('Order', backref='product')
    reviews = db.relationship('Review', backref='product')
