import os


# class Config(object):
#     DEBUG = False
#
#
# class DevelopmentConfig(Config):
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SQLALCHEMY_ECHO = True
#
#
# class ProductionConfig(Config):
#     DEBUG = False
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SQLALCHEMY_ECHO = False
#
#
# class TestingConfig(Config):
#     TESTING = True
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
#     SQLALCHEMY_TRACK_MODIFICATIONS = True
#     SQLALCHEMY_ECHO = True


# config_by_name = {
#     'dev': DevelopmentConfig,
#     'prod': ProductionConfig,
#     'test': TestingConfig
# }

MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = True
MAIL_USERNAME = "316710519@qq.com"
MAIL_PASSWORD = "frvicghahgzpbhih"
MAIL_DEFAULT_SENDER = "316710519@qq.com"

SECRET_KEY = "20020413gzq"  # config secret key
