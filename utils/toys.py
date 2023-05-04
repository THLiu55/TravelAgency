from flask import session
import hashlib
import datetime


### BABEL RELATED ###
def get_locale():
    return session.get("language", "en")


### END BABEL RELATED ###


### CHAT RELATED ###
def get_fuzzed_room_name(customer_id):
    # my impl is to hash the customer_id to get a room name
    return hashlib.sha256(str(customer_id).encode("utf-8")).hexdigest()[:10]

def hash_filename(filename):
    ext = filename.split(".")[-1]
    filename_without_ext = filename[: -len(ext) - 1]
    to_hash = filename_without_ext + str(datetime.datetime.now())
    return hashlib.sha256(to_hash.encode("utf-8")).hexdigest() + "." + ext

### END CHAT RELATED ###


def extract_date(datetime_string):
    # Remove the timezone information
    datetime_string = datetime_string.split()[0]

    # Convert the string to a datetime object
    datetime_obj = datetime.datetime.fromisoformat(datetime_string)

    # Extract the date portion and format it as "yyyy-mm-dd"
    formatted_date = datetime_obj.strftime("%Y-%m-%d")

    return formatted_date
