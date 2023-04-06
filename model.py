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
    activity_orders = db.relationship('ActivityOrder', backref='customer')
    activity_reviews = db.relationship('ActivityReview', backref='customer')
    tour_orders = db.relationship('TourOrder', backref='customer')
    tour_reviews = db.relationship('TourReview', backref='customer')
    hotel_orders = db.relationship('HotelOrder', backref='customer')
    hotel_reviews = db.relationship('HotelReview', backref='customer')
    flight_orders = db.relationship('FlightOrder', backref='customer')
    flight_reviews = db.relationship('FlightReview', backref='customer')
    messages = db.relationship('Message', backref='customer')


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    postTime = db.Column(db.DateTime)
    isRead = db.Column(db.Boolean)
    sendByCustomer = db.Column(db.Boolean)
    customerID = db.Column(db.Integer, db.ForeignKey('customers.id'))


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
    view_num = db.Column(db.Integer)
    review = db.relationship('ActivityReview', backref='product')
    orders = db.relationship('ActivityOrder', backref='product')

    def serialize(self):
        return {
            'id': self.id,
            'category': self.category,
            'status': self.status,
            'name': self.name,
            'start_time': self.start_time,
            'price': self.price
        }

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'status': self.status,
            'price': self.price,
            'city': self.city,
            'state': self.state,
            'address': self.address,
            'duration': self.duration,
            'group_size': self.group_size,
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S') if self.start_time else None,
            'end_time': self.end_time.strftime('%Y-%m-%d %H:%M:%S') if self.end_time else None,
            'images': self.images,
            'description': self.description,
            'included': self.included,
            'excluded': self.excluded,
            'openHour': self.openHour.strftime('%H:%M:%S') if self.openHour else None,
            'visitHour': self.visitHour,
            'total_star': self.total_star,
            'review_num': self.review_num,
            'star_detail': self.star_detail,
            'contact_name': self.contact_name,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
        }


class TourOrder(db.Model):
    __tablename__ = 'tour_orders'

    id = db.Column(db.Integer, primary_key=True)
    startTime = db.Column(db.DateTime)
    endTime = db.Column(db.DateTime)
    cost = db.Column(db.Float)
    purchased = db.Column(db.Boolean)
    productID = db.Column(db.Integer, db.ForeignKey('tours.id'))
    customerID = db.Column(db.Integer, db.ForeignKey('customers.id'))


class TourReview(db.Model):
    __tablename__ = 'tour_reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    issueTime = db.Column(db.DateTime)
    content = db.Column(db.Text)
    customerID = db.Column(db.Integer, db.ForeignKey('customers.id'))
    productID = db.Column(db.Integer, db.ForeignKey('tours.id'))


class Tour(db.Model):
    __tablename__ = 'tours'
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
    itineraries = db.Column(db.Text)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    images = db.Column(db.Text)
    description = db.Column(db.Text)
    included = db.Column(db.Text)
    excluded = db.Column(db.Text)
    total_star = db.Column(db.Integer)
    review_num = db.Column(db.Integer)
    star_detail = db.Column(db.Text)
    contact_name = db.Column(db.String(255))
    contact_email = db.Column(db.String(255))
    contact_phone = db.Column(db.String(255))
    view_num = db.Column(db.Integer)
    review = db.relationship('TourReview', backref='product')
    orders = db.relationship('TourOrder', backref='product')

    def serialize(self):
        return {
            'id': self.id,
            'category': self.category,
            'status': self.status,
            'name': self.name,
            'start_time': self.start_time,
            'price': self.price
        }

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'price': self.price,
            'city': self.city,
            'state': self.state,
            'address': self.address,
            'images': self.images,
            'total_star': self.total_star,
            'review_num': self.review_num,
            'star_detail': self.star_detail,
        }


class Hotel(db.Model):
    __tablename__ = 'hotels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    status = db.Column(db.String(255))
    min_price = db.Column(db.Float)
    room_num = db.Column(db.Integer)
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    address = db.Column(db.Text)
    min_stay = db.Column(db.String(255))
    security = db.Column(db.String(255))
    on_site_staff = db.Column(db.String(255))
    house_keeping = db.Column(db.String(255))
    front_desk = db.Column(db.String(255))
    bathroom = db.Column(db.String(255))
    room_type_num = db.Column(db.Integer)
    images = db.Column(db.Text)
    description = db.Column(db.Text)
    room_detail = db.Column(db.Text)
    amenities = db.Column(db.Text)
    total_star = db.Column(db.Integer)
    review_num = db.Column(db.Integer)
    star_detail = db.Column(db.Text)
    contact_name = db.Column(db.String(255))
    contact_email = db.Column(db.String(255))
    contact_phone = db.Column(db.String(255))
    view_num = db.Column(db.Integer)
    review = db.relationship('HotelReview', backref='product')
    orders = db.relationship('HotelOrder', backref='product')

    def serialize(self):
        return {
            'id': self.id,
            'status': self.status,
            'name': self.name,
            'price': self.min_price,
            'city': self.city,
            'room_num': self.room_num
        }


class HotelOrder(db.Model):
    __tablename__ = 'hotel_orders'

    id = db.Column(db.Integer, primary_key=True)
    startTime = db.Column(db.DateTime)
    endTime = db.Column(db.DateTime)
    cost = db.Column(db.Float)
    purchased = db.Column(db.Boolean)
    productID = db.Column(db.Integer, db.ForeignKey('hotels.id'))
    customerID = db.Column(db.Integer, db.ForeignKey('customers.id'))


class HotelReview(db.Model):
    __tablename__ = 'hotel_reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    issueTime = db.Column(db.DateTime)
    content = db.Column(db.Text)
    customerID = db.Column(db.Integer, db.ForeignKey('customers.id'))
    productID = db.Column(db.Integer, db.ForeignKey('hotels.id'))


class Flight(db.Model):
    __tablename__ = 'flights'

    id = db.Column(db.Integer, primary_key=True)
    flight_type = db.Column(db.String(255))
    takeoff_time = db.Column(db.DateTime)
    landing_time = db.Column(db.DateTime)
    flight_stop = db.Column(db.Integer)
    company = db.Column(db.String(255))
    total_time = db.Column(db.Float)
    price = db.Column(db.Float)
    fare_type = db.Column(db.String(255))
    flight_class = db.Column(db.String(255))
    cancellation_charge = db.Column(db.String(255))
    change_charge = db.Column(db.String(255))
    seat_baggage = db.Column(db.String(255))
    base_fare = db.Column(db.String(255))
    taxes = db.Column(db.String(255))
    images = db.Column(db.Text)
    description = db.Column(db.Text)
    inflight_features = db.Column(db.Text)
    total_star = db.Column(db.Integer)
    review_num = db.Column(db.Integer)
    star_detail = db.Column(db.Text)
    contact_name = db.Column(db.String(255))
    contact_email = db.Column(db.String(255))
    contact_phone = db.Column(db.String(255))
    view_num = db.Column(db.Integer)
    review = db.relationship('FlightReview', backref='product')
    orders = db.relationship('FlightOrder', backref='product')


class FlightOrder(db.Model):
    __tablename__ = 'flight_orders'

    id = db.Column(db.Integer, primary_key=True)
    startTime = db.Column(db.DateTime)
    endTime = db.Column(db.DateTime)
    cost = db.Column(db.Float)
    purchased = db.Column(db.Boolean)
    productID = db.Column(db.Integer, db.ForeignKey('flights.id'))
    customerID = db.Column(db.Integer, db.ForeignKey('customers.id'))


class FlightReview(db.Model):
    __tablename__ = 'flight_reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    issueTime = db.Column(db.DateTime)
    content = db.Column(db.Text)
    customerID = db.Column(db.Integer, db.ForeignKey('customers.id'))
    productID = db.Column(db.Integer, db.ForeignKey('flights.id'))