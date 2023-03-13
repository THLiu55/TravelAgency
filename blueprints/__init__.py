from .customer import bp as customer_bp


def bp_register_all(app):
    app.register_blueprint(customer_bp)
