from functools import wraps

from flask import session, redirect, url_for, request


def login_required(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        if session.get('customer_id') is None:
            url = request.url
            return redirect(url_for('customer.login', url=url))
        return function(*args, **kwargs)
    return decorator


def staff_login_required(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        if session.get('staff_id') is None:
            url = request.url
            print(url)
            return redirect(url_for('manager.login', url=url))
        return function(*args, **kwargs)
    return decorator