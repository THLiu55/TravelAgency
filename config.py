import os
from dotenv import load_dotenv


class Config(object):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_TLS = bool(os.getenv('MAIL_USE_TLS'))
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL')
    MAIL_DEBUG = os.getenv('MAIL_DEBUG')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    SECRET_KEY = os.getenv('SECRET_KEY')



class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True


config_by_name = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
    'test': TestingConfig
}


BABEL_DEFAULT_LOCALE = 'zh'
BABEL_DEFAULT_TIMEZONE = 'UTC'
LANGUAGES = {
    'en': 'English',
    'zh': 'Chinese'
}