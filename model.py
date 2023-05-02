from exts import db
from flask_login import UserMixin
from utils.toys import extract_date


class Customer(db.Model, UserMixin):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    nickname = db.Column(db.String(255))
    password = db.Column(db.String(255))
    avatarURL = db.Column(db.Text)
    wallet = db.Column(db.Double)
    join_date = db.Column(db.DateTime)
    address = db.Column(db.Text)
    phone_number = db.Column(db.String(255))
    amount_unread_msgs = db.Column(db.Integer, default=0)
    activity_orders = db.relationship('ActivityOrder', backref='customer')
    activity_reviews = db.relationship('ActivityReview', backref='customer')
    tour_orders = db.relationship('TourOrder', backref='customer')
    tour_reviews = db.relationship('TourReview', backref='customer')
    hotel_orders = db.relationship('HotelOrder', backref='customer')
    hotel_reviews = db.relationship('HotelReview', backref='customer')
    flight_orders = db.relationship('FlightOrder', backref='customer')
    flight_reviews = db.relationship('FlightReview', backref='customer')
    messages = db.relationship('Message', backref='customer')

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'nickname': self.nickname,
            'avatar': self.avatarURL,
            'wallet': self.wallet
        }


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    isPic = db.Column(db.Boolean)
    content = db.Column(db.Text)
    sentTime = db.Column(db.DateTime)
    isByCustomer = db.Column(db.Boolean)  # if False then by staff
    customerID = db.Column(db.Integer, db.ForeignKey('customers.id'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'isPic': self.isPic,
            'content': self.content,
            'sentTime': self.sentTime.strftime("%Y-%m-%d %H:%M:%S"),
            'isByCustomer': self.isByCustomer,
            'customerID': self.customerID,
        }


class ActivityOrder(db.Model):
    __tablename__ = 'activity_orders'

    id = db.Column(db.Integer, primary_key=True)
    startTime = db.Column(db.DateTime)  # order time
    endTime = db.Column(db.DateTime)
    cost = db.Column(db.Float)
    purchased = db.Column(db.Boolean)
    productID = db.Column(db.Integer, db.ForeignKey('activities.id'))
    customerID = db.Column(db.Integer, db.ForeignKey('customers.id'))

    def serialize(self):
        return {
            'customer': self.customer.serialize(),
            'category': 'activity',
            'id': self.id,
            'start_time': self.startTime.isoformat(),
            'end_time': self.endTime.isoformat(),
            'cost': self.cost,
            'purchased': self.purchased
        }


class ActivityReview(db.Model):
    __tablename__ = 'activity_reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    issueTime = db.Column(db.DateTime)
    content = db.Column(db.Text)
    customerID = db.Column(db.Integer, db.ForeignKey('customers.id'))
    productID = db.Column(db.Integer, db.ForeignKey('activities.id'))

    def serialize(self):
        return {
            'category': 'activity',
            'reviewed_product': self.product.serialize(),
            'customer': self.customer.serialize(),
            'rating': self.rating,
            'content': self.content,
            'date': extract_date(self.issueTime.isoformat())
        }


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
    review_num = db.Column(db.Integer, default=0)
    star_detail = db.Column(db.Text)
    contact_name = db.Column(db.String(255))
    contact_email = db.Column(db.String(255))
    contact_phone = db.Column(db.String(255))
    view_num = db.Column(db.Integer, default=0)
    lat = db.Column(db.Double)
    lon = db.Column(db.Double)
    review = db.relationship('ActivityReview', backref='product')
    orders = db.relationship('ActivityOrder', backref='product')

    def serialize(self):
        return {
            'id': self.id,
            'category': self.category,
            'status': self.status,
            'name': self.name,
            'start_time': self.start_time.isoformat(),
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

    def serialize_info(self):
        return {
            'name': self.name,
            'category': self.category,
            'status': self.status,
            'price': self.price,
            'city': self.city,
            'state': self.state,
            'address': self.address,
            'duration': self.duration,
            'group_size': self.group_size,
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': self.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'images': self.images.split(',') if self.images else [],
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
            'view_num': self.view_num,
            'lat': self.lat,
            'lon': self.lon
        }


class TourOrder(db.Model):
    __tablename__ = 'tour_orders'

    id = db.Column(db.Integer, primary_key=True)
    startTime = db.Column(db.DateTime)  # order time
    endTime = db.Column(db.DateTime)
    cost = db.Column(db.Float)
    purchased = db.Column(db.Boolean)
    productID = db.Column(db.Integer, db.ForeignKey('tours.id'))
    customerID = db.Column(db.Integer, db.ForeignKey('customers.id'))

    def serialize(self):
        return {
            'customer': self.customer.serialize(),
            'category': 'tour',
            'id': self.id,
            'start_time': self.startTime.isoformat(),
            'end_time': self.endTime.isoformat(),
            'cost': self.cost,
            'purchased': self.purchased
        }


class TourReview(db.Model):
    __tablename__ = 'tour_reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    issueTime = db.Column(db.DateTime)
    content = db.Column(db.Text)
    customerID = db.Column(db.Integer, db.ForeignKey('customers.id'))
    productID = db.Column(db.Integer, db.ForeignKey('tours.id'))

    def serialize(self):
        return {
            'category': 'tour',
            'reviewed_product': self.product.serialize(),
            'customer': self.customer.serialize(),
            'rating': self.rating,
            'content': self.content,
            'date': extract_date(self.issueTime.isoformat())
        }


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
    view_num = db.Column(db.Integer, default=0)
    star_detail = db.Column(db.Text)
    contact_name = db.Column(db.String(255))
    contact_email = db.Column(db.String(255))
    contact_phone = db.Column(db.String(255))
    review_num = db.Column(db.Integer, default=0)
    review = db.relationship('TourReview', backref='product')
    orders = db.relationship('TourOrder', backref='product')

    def serialize(self):
        return {
            'id': self.id,
            'category': self.category,
            'status': self.status,
            'name': self.name,
            'start_time': self.start_time.isoformat(),
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
            "contact_email": self.contact_email
        }

    def serialize_info(self):
        # Create a dictionary with all the information except for the id
        return {
            "name": self.name,
            "category": self.category,
            "status": self.status,
            "price": self.price,
            "city": self.city,
            "state": self.state,
            "address": self.address,
            "duration": self.duration,
            "group_size": self.group_size,
            "itineraries": self.itineraries,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "images": self.images,
            "description": self.description,
            "included": self.included,
            "excluded": self.excluded,
            "total_star": self.total_star,
            "view_num": self.view_num,
            "star_detail": self.star_detail,
            "contact_name": self.contact_name,
            "contact_email": self.contact_email,
            "contact_phone": self.contact_phone,
            "review_num": self.review_num
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
    star = db.Column(db.String(255))
    room_type_num = db.Column(db.Integer)
    images = db.Column(db.Text)
    description = db.Column(db.Text)
    room_detail = db.Column(db.Text)
    amenities = db.Column(db.Text)
    total_star = db.Column(db.Integer)
    review_num = db.Column(db.Integer, default=0)
    star_detail = db.Column(db.Text)
    contact_name = db.Column(db.String(255))
    contact_email = db.Column(db.String(255))
    contact_phone = db.Column(db.String(255))
    view_num = db.Column(db.Integer, default=0)
    lat = db.Column(db.Double)
    lon = db.Column(db.Double)
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

    def to_dict(self):
        return {
            "id": self.id,
            'images': self.images,
            "name": self.name,
            "address": self.address,
            "city": self.city,
            "review_num": self.review_num,
            "min_price": self.min_price,
            "contact_email": self.contact_email,
        }

    def serialize_info(self):
        serialized_hotel = {
            "name": self.name,
            "status": self.status,
            "min_price": self.min_price,
            "room_num": self.room_num,
            "city": self.city,
            "state": self.state,
            "address": self.address,
            "min_stay": self.min_stay,
            "security": self.security,
            "on_site_staff": self.on_site_staff,
            "house_keeping": self.house_keeping,
            "front_desk": self.front_desk,
            "bathroom": self.bathroom,
            "star": self.star,
            "room_type_num": self.room_type_num,
            "images": self.images,
            "description": self.description,
            "room_detail": self.room_detail,
            "amenities": self.amenities,
            "total_star": self.total_star,
            "review_num": self.review_num,
            "star_detail": self.star_detail,
            "contact_name": self.contact_name,
            "contact_email": self.contact_email,
            "contact_phone": self.contact_phone,
            "view_num": self.view_num,
            "lat": self.lat,
            "lon": self.lon
        }
        return serialized_hotel


class HotelOrder(db.Model):
    __tablename__ = 'hotel_orders'

    id = db.Column(db.Integer, primary_key=True)
    startTime = db.Column(db.DateTime)  # check in time
    endTime = db.Column(db.DateTime)  # Order time
    checkOutTime = db.Column(db.DateTime)  # check out time
    cost = db.Column(db.Float)
    purchased = db.Column(db.Boolean)
    roomID = db.Column(db.String(255))
    productID = db.Column(db.Integer, db.ForeignKey('hotels.id'))
    customerID = db.Column(db.Integer, db.ForeignKey('customers.id'))

    def serialize(self):
        return {
            'customer': self.customer.serialize(),
            'category': 'hotel',
            'id': self.id,
            'start_time': self.startTime.isoformat(),
            'end_time': self.checkOutTime.isoformat(),
            'cost': self.cost,
            'purchased': self.purchased
        }


class HotelReview(db.Model):
    __tablename__ = 'hotel_reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    issueTime = db.Column(db.DateTime)
    content = db.Column(db.Text)
    roomID = db.Column(db.String(255))
    customerID = db.Column(db.Integer, db.ForeignKey('customers.id'))
    productID = db.Column(db.Integer, db.ForeignKey('hotels.id'))

    def serialize(self):
        return {
            'category': 'hotel',
            'reviewed_product': self.product.serialize(),
            'customer': self.customer.serialize(),
            'rating': self.rating,
            'content': self.content,
            'date': extract_date(self.issueTime.isoformat())
        }


class Flight(db.Model):
    __tablename__ = 'flights'

    id = db.Column(db.Integer, primary_key=True)
    departure = db.Column(db.String(255))
    destination = db.Column(db.String(255))
    status = db.Column(db.String(255))
    flight_type = db.Column(db.String(255))
    week_day = db.Column(db.Integer)
    takeoff_time = db.Column(db.Time)
    landing_time = db.Column(db.Time)
    flight_stop = db.Column(db.String(255))
    company = db.Column(db.String(255))
    total_time = db.Column(db.Float)
    price = db.Column(db.Float)
    fare_type = db.Column(db.String(255))
    flight_class = db.Column(db.String(255))
    cancellation_charge = db.Column(db.String(255))
    flight_charge = db.Column(db.String(255))
    seat_baggage = db.Column(db.String(255))
    base_fare = db.Column(db.String(255))
    taxes = db.Column(db.String(255))
    images = db.Column(db.Text)
    description = db.Column(db.Text)
    inflight_features = db.Column(db.Text)
    total_star = db.Column(db.Integer)
    review_num = db.Column(db.Integer, default=0)
    star_detail = db.Column(db.Text)
    contact_name = db.Column(db.String(255))
    contact_email = db.Column(db.String(255))
    contact_phone = db.Column(db.String(255))
    view_num = db.Column(db.Integer, default=0)
    review = db.relationship('FlightReview', backref='product')
    orders = db.relationship('FlightOrder', backref='product')

    def serialize(self):
        return {
            'id': self.id,
            'status': self.status,
            'departure': self.departure,
            'destination': self.destination,
            'take_off_time': self.takeoff_time.isoformat(),
            'landing_time': self.landing_time.isoformat()
        }

    def to_dict(self):
        return {
            'company': self.company,
            'takeoff_time': self.takeoff_time.strftime("%H:%M"),
            'flight_stop': self.flight_stop,
            'landing_time': self.landing_time.strftime("%H:%M"),
            'destination': self.destination,
            'total_time': self.total_time,
            'price': self.price,
            'fare_type': self.fare_type,
            'departure': self.departure,
            'contact_name': self.contact_name,
            'images': self.images
        }

    def serialize_info(self):
        info = {
            'departure': self.departure,
            'destination': self.destination,
            'status': self.status,
            'flight_type': self.flight_type,
            'week_day': self.week_day,
            'takeoff_time': str(self.takeoff_time),
            'landing_time': str(self.landing_time),
            'flight_stop': self.flight_stop,
            'company': self.company,
            'total_time': self.total_time,
            'price': self.price,
            'fare_type': self.fare_type,
            'flight_class': self.flight_class,
            'cancellation_charge': self.cancellation_charge,
            'flight_charge': self.flight_charge,
            'seat_baggage': self.seat_baggage,
            'base_fare': self.base_fare,
            'taxes': self.taxes,
            'images': self.images,
            'description': self.description,
            'inflight_features': self.inflight_features,
            'total_star': self.total_star,
            'review_num': self.review_num,
            'star_detail': self.star_detail,
            'contact_name': self.contact_name,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'view_num': self.view_num,
        }
        return info


class FlightOrder(db.Model):
    __tablename__ = 'flight_orders'

    id = db.Column(db.Integer, primary_key=True)
    startTime = db.Column(db.DateTime)  # order time
    endTime = db.Column(db.DateTime)
    cost = db.Column(db.Float)
    purchased = db.Column(db.Boolean)
    productID = db.Column(db.Integer, db.ForeignKey('flights.id'))
    customerID = db.Column(db.Integer, db.ForeignKey('customers.id'))

    def serialize(self):
        return {
            'customer': self.customer.serialize(),
            'category': 'flight',
            'id': self.id,
            'start_time': self.startTime.isoformat(),
            'end_time': self.endTime.isoformat(),
            'cost': self.cost,
            'purchased': self.purchased
        }


class FlightReview(db.Model):
    __tablename__ = 'flight_reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    issueTime = db.Column(db.DateTime)
    content = db.Column(db.Text)
    customerID = db.Column(db.Integer, db.ForeignKey('customers.id'))
    productID = db.Column(db.Integer, db.ForeignKey('flights.id'))


class Room:
    square_1 = False
    square_2 = False
    bed_1 = False
    bed_2 = False
    wifi = False
    shower = False
    free = False
    picture = ''
    price = 0


class OrderObject:
    name = ''
    type = ''
    date = ''
    price = ''
    status = True  # finish
    url = ''
    time = None


class PlanObj:
    title = ''
    start = None
    end = None
    color = ''


class WishListObject:
    def __init__(self, title, second_line, star, star_des, review_num, price, photo_url, url, time, type_, id):
        self.title = title
        self.second_line = second_line
        self.star = star
        self.star_des = star_des
        self.review_num = review_num
        self.price = price
        self.photo_url = photo_url
        self.url = url
        self.time = time
        self.type_ = type_
        self.id = id