import json
from datetime import datetime

from flask import Blueprint, render_template, request, jsonify, current_app, session
from model import *
from exts import db


bp = Blueprint("activity", __name__, url_prefix="/tour")

@bp.route("/")
def tour():
    return render_template("")
