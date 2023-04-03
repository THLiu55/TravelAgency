import os


class Config(object):
    DEBUG = False

    # SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.getenv("DB_URI")
    # SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.getenv("ENV_NAME") + ".sqlite3"
    SQLALCHEMY_DATABASE_URI = r"sqlite:///C:\project2\travelagency\travelAgency.db"
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = (
        int(os.getenv("MAIL_PORT")) if os.getenv("MAIL_PORT") is not None else 25
    )
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS") == "True"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL") == "True"
    MAIL_DEBUG = (
        int(os.getenv("MAIL_DEBUG")) if os.getenv("MAIL_DEBUG") is not None else 0
    )
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    SECRET_KEY = os.getenv("SECRET_KEY")

    BABEL_DEFAULT_LOCALE = "zh"
    BABEL_DEFAULT_TIMEZONE = "UTC"
    LANGUAGES = {"en": "English", "zh": "Chinese"}


class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    DEBUG = False
    USE_CLOUD_DATABASE = os.getenv("USE_CLOUD_DATABASE") == "True"
    # TODO: cloud database support
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True


config_by_name = {
    "dev": DevelopmentConfig,
    "prod": ProductionConfig,
    "test": TestingConfig,
}
