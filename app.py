import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, session, request, make_response, jsonify, send_from_directory, g
from dotenv import load_dotenv
from config import config_by_name
from blueprints import bp_register_all
from exts import exts_load_all

from flask_babel import Babel, gettext as _, refresh

load_dotenv()

# app config
app = Flask(__name__, static_folder='static')
app.config.from_object(config_by_name[os.getenv("ENV_NAME")])
print(os.getenv("ENV_NAME"))

# logger config
handler = RotatingFileHandler("./logs/app.log", maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s"
)
handler.setFormatter(formatter)
app.logger.addHandler(handler)

# blueprints and extensions
bp_register_all(app)
exts_load_all(app)

session.setdefault("language", "en")

# global decorators
@app.before_request
def before_request():
    '''this is the hook before every request'''

    if "customer_id" in session:
        g.customer_id = session.get("customer_id")
    
    if "staff_id" in session:
        g.staff_id = session.get("staff_id")
        g.admin_username = os.environ.get("ADMIN_USERNAME")

    return

@app.after_request
def after_request(response):
    '''this is the hook after every request'''
    return response


@app.route("/set_locale")
def set_locale():
    lang = request.args.get("language")
    print(lang)
    response = make_response(jsonify(message=lang))
    if lang == "en":
        session["language"] = "en"
        refresh()
        return response
    if lang == "zh":
        session["language"] = "zh"
        refresh()
        return response
    return jsonify({"data": "success"})


# @app.context_processor
# def inject_conf_var():
#     return dict(AVAILABLE_LANGUAGES=app.config['LANGUAGES'], CURRENT_LANGUAGE=session.get('language', request.accept_languages.best_match(app.config['LANGUAGES'].keys())))


@app.route('/<path:filename>')
def node_file_for_search(filename):
    return send_from_directory(app.root_path, filename)


@app.route('/<path:filename>')
def node_file_for_map(filename):
    return send_from_directory(app.root_path, filename)


if __name__ == "__main__":
    app.run()
