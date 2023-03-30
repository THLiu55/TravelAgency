import json
from datetime import datetime

from flask import Blueprint, render_template, request, jsonify, current_app, session
from model import *
from exts import db
import os

bp = Blueprint("tour", __name__, url_prefix="/tour")

