from flask import session
import hashlib


# babel related
def get_locale():
    return session.get("language", "zh")


### CHAT RELATED ###
def get_fuzzed_room_name(customer_id):
    # my impl is to hash the customer_id to get a room name
    # return hashlib.sha256(str(customer_id).encode("utf-8")).hexdigest()[:10]
    return customer_id # for test