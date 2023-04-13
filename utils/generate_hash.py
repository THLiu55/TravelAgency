import datetime
import hashlib


def hash_text(text):
    return str(hashlib.md5(text.encode()).hexdigest())[0:6]


def get_hash_time(email):
    now = datetime.datetime.now()
    email = email + str(now.year) + str(now.month) + str(now.day) + str(now.hour)
    return hash_text(email)


def check_hash_time(email, captcha):
    now = datetime.datetime.now()
    hash_value1 = hash_text(email + str(now.year) + str(now.month) + str(now.day) + str(now.hour))
    if now.hour == 0:
        hash_value2 = hash_text(email + str(now.year) + str(now.month) + str(now.day - 1) + str(23))
    else:
        hash_value2 = hash_text(email + str(now.year) + str(now.month) + str(now.day) + str(now.hour - 1))
    return hash_value1 == captcha or hash_value2 == captcha
