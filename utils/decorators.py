from functools import wraps

from flask import session, redirect, url_for


def login_required(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        if session.get('customer_id') is None:
            return redirect(url_for('customer.login'))
        return function(*args, **kwargs)
    return decorator
