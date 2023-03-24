from .customer import bp as customer_bp
from .activity import bp as activity_bp
from .manager import bp as manager_bp


def bp_register_all(app):
    app.register_blueprint(customer_bp)
    app.register_blueprint(activity_bp)
    app.register_blueprint(manager_bp)