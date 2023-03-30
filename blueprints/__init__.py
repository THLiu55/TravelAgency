from .customer import bp as customer_bp
from .activity import bp as activity_bp
from .chat import bp as chat_bp
from .manager import bp as manager_bp
from .tour import bp as tour_bp


def bp_register_all(app):
    app.register_blueprint(customer_bp)
    app.register_blueprint(activity_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(manager_bp)
    app.register_blueprint(tour_bp)
