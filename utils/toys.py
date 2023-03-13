from flask import session

# babel related
def get_locale():
    return session.get("language", "zh")