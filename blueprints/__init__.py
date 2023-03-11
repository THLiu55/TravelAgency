from .customer import bp as customer_bp


def bp_register(app):
    app.register_blueprint(customer_bp)
