from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flask_babel import Babel, gettext as _, refresh
from flask_socketio import SocketIO, emit
from sqlalchemy import MetaData

from utils.toys import get_locale


mail = Mail()
babel = Babel()
socketio = SocketIO()

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention), session_options={"autoflush": False})
migrate = Migrate(render_as_batch=True)


def exts_load_all(app):
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    babel.init_app(app, locale_selector=get_locale)
    socketio.init_app(app, cors_allowed_origins="*")



