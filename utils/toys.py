from flask import session
import hashlib
import datetime
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

SECRET_KEY = os.environ.get("SECRET_KEY")


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


### CDKEY RELATED ###


def get_cipher():
    key = SECRET_KEY.encode("utf-8")
    if len(key) > 16:
        key = key[:16]
    elif len(key) < 16:
        key = key + b"\x00" * (16 - len(key))
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher


def generate_pile_of_cdkeys(cipher, date_str, start_idx, end_idx, value):
    cdkeys = []
    date_str = date_str.replace("-", "")
    four_digit_value = str(value).zfill(4)
    for i in range(start_idx, end_idx):
        eight_digit_idx = str(i).zfill(8)
        cdkeys.append(
            generate_cdkey(cipher, date_str, eight_digit_idx, four_digit_value)
        )
    return cdkeys


def generate_cdkey(cipher, date_str, cdk_index_str, value_str):
    seed = date_str + cdk_index_str + value_str
    if len(seed) != 20:
        raise ValueError("Invalid seed length")
    padded_seed = pad(seed.encode("utf-8"), AES.block_size)
    encrypted_seed = cipher.encrypt(padded_seed)
    # then we convert the encrypted seed to url-safe base64 string
    cdkey = base64.urlsafe_b64encode(encrypted_seed).decode("utf-8")
    return cdkey # cdkey is a 24 bytes string


def decrypt_cdkey(cipher, cdkey):
    encrypted_seed = base64.urlsafe_b64decode(cdkey.encode("utf-8"))
    padded_seed = cipher.decrypt(encrypted_seed)
    seed = unpad(padded_seed, AES.block_size).decode("utf-8")
    date_str = seed[:8]
    serial_str = seed[8:16]
    value_str = seed[16:]
    return date_str, serial_str, value_str


def validate_decrypted_attrs(dec_date_str, dec_serial_str, dec_value_str):
    if len(dec_date_str) != 8: # because no dashes
        return False
    elif len(dec_serial_str) != 8:
        return False
    elif len(dec_value_str) != 4:
        return False
    else:
        try:
            datetime.datetime.strptime(dec_date_str, "%Y%m%d")
            # print("date is valid with value: " + dec_date_str)
        except ValueError:
            return False
        try:
            int(dec_serial_str)
            # print("serial is valid with value: " + dec_serial_str)
        except ValueError:
            return False
        try:
            int(dec_value_str)
            # print("value is valid with value: " + dec_value_str)
        except ValueError:
            return False
        return True

### END CDKEY RELATED ###


### TEST TRASH CODE
# test_cdkey = generate_cdkey(get_cipher(), "20230505", "00000001", "2333")
# print("test_cdkey: " + test_cdkey)

# test_cdkey_list = generate_pile_of_cdkeys(get_cipher(), "20230505", 1, 10, 2333)
# for cdkey in test_cdkey_list:
#     print(cdkey)

# a, b, c = decrypt_cdkey(get_cipher(), test_cdkey)
# if validate_decrypted_attrs( a, b, c ):
#     print("validation passed")
# else:
#     print("validation failed")
