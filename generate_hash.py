import datetime


def hash_text(text):
    return str(hash(text)).lstrip('-')[0:6]


def get_hash_time(email):
    now = datetime.datetime.now()
    email = email + str(now.year) + str(now.month) + str(now.hour)
    return hash_text(email)


def check_hash_time(email, captcha):
    now = datetime.datetime.now()
    hash_value1 = hash_text(email + str(now.year) + str(now.month) + str(now.hour))
    if now.hour == 23:
        hash_value2 = hash_text(email + str(now.year) + str(now.month) + str(1))
    else:
        hash_value2 = hash_text(email + str(now.year) + str(now.month) + str(now.hour-1))
    return hash_value1 == captcha or hash_value2 == captcha
