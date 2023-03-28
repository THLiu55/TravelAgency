from flask import Blueprint, request, render_template, g, redirect, url_for

# from decorators import login_required
from exts import db, socketio
from utils.bot import get_wxbot_signature, get_wxbot_answer
from model import Customer
from time import time

bp = Blueprint("chat", __name__, url_prefix="/")

name_space = "/socketest"


@bp.route("/get_chatbot_answer", methods=["POST"])
def get_chatbot_answer():
    if request.method == "POST":
        message = request.form["msg"]
        # if not g.user:
        #     return "Please login first."

        userid = "test" # TODO: this is a test user id, should be replaced by the real user id

        # if g.user:
        #     if g.user.signature and time() - g.user.signature_timestamp < 7200:
        #         signature = g.user.signature

        signature = get_wxbot_signature(userid)  # this will expire in 7200 seconds

        # TODO: refactor this to make it use the cached signature withing 7200 seconds rather than requesting a new one every time

        # userid = (
        #     g.user.id if g.user else "guest_" + str(Customer.query.count())
        #     # TODO: guest_1, guest_2, guest_3, ... is not a good way to identify a guest
        # )

        answer = get_wxbot_answer(message, signature)
        return answer


def ack():
    print("ack")


@socketio.on("connect", namespace=name_space)
def connected_msg():
    print("client connected.")


@socketio.on("disconnect", namespace=name_space)
def disconnect_msg():
    print("client disconnected.")


@socketio.on("message", namespace=name_space)
def message_msg(data):
    sender_name = data["sender"]
    msg_itself = data["msg"]
    sending_data = {"sender": sender_name, "msg": msg_itself}
    socketio.emit("message", sending_data, broadcast=False, namespace=name_space)


@socketio.on("my_event", namespace=name_space)
def mtest_message(message):
    print(message)
    socketio.emit("my_response", str({"data": message["data"], "count": 1}))
