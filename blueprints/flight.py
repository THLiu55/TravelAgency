import json

from flask import Blueprint, session, render_template
from model import Flight, FlightOrder, FlightReview

bp = Blueprint("flight", __name__, url_prefix="/flight")


@bp.route('/<page_num>', methods=['POST', 'GET'])
def flightList(page_num):
    logged = False if session.get('customer_id') is None else True
    total_flights = Flight.query.count()
    pagination = Flight.query.paginate(page=int(page_num), per_page=9, error_out=False)
    flights = pagination.items
    for flight in flights:
        # noinspection PyTypeChecker
        flight.images = json.loads(flight.images)['images']
        flight.images[0] = flight.images[0][flight.images[0].index('static'):].lstrip('static')
    return render_template("flight.html")
