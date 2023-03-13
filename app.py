from flask import Flask, render_template, session, request, make_response, jsonify
from flask_babel import Babel, gettext as _, refresh

from blueprints import bp_register
import config
from exts import db, mail
from flask_migrate import Migrate
from model import *


app = Flask(__name__)
bp_register(app)
app.config.from_object(config)
app.config['DATABASE'] = 'travelAgency'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\SQLite\\travelAgency.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
mail.init_app(app)
db.init_app(app)
migrate = Migrate(app, db)

# translations
babel = Babel(app=app)


def get_locale():
    print(session.get('language', 'zh'))
    return session.get('language', 'zh')


babel.init_app(app, locale_selector=get_locale)


@app.route("/set_locale")
def set_locale():
    lang = request.args.get("language")
    print(lang)
    response = make_response(jsonify(message=lang))
    if lang == 'en':
        session['language'] = 'en'
        refresh()
        return response
    if lang == 'zh':
        session['language'] = 'zh'
        refresh()
        return response
    return jsonify({"data": "success"})


@app.context_processor
def inject_conf_var():
    return dict(AVAILABLE_LANGUAGES=app.config['LANGUAGES'], CURRENT_LANGUAGE=session.get('language', request.accept_languages.best_match(app.config['LANGUAGES'].keys())))


@app.route('/')
def hello_world():  # put application's code here
    # return render_template("ProductsDetail.html")
    return render_template("SignInUp.html")
    # return render_template("Homepage.html")


if __name__ == '__main__':
    app.run()
