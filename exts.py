from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flask_babel import Babel, gettext as _, refresh
from flask_socketio import SocketIO, emit

from utils.toys import get_locale

db = SQLAlchemy(session_options={"autoflush": False})
mail = Mail()
migrate = Migrate()
babel = Babel()
socketio = SocketIO()


def exts_load_all(app):
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    babel.init_app(app, locale_selector=get_locale)
    socketio.init_app(app, cors_allowed_origins="*")
