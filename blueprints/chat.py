from flask import Blueprint, request, render_template, g, redirect, url_for, session

# from decorators import login_required
from exts import db, socketio
from utils.bot import BOT_CHOICE, get_wxbot_signature, get_wxbot_answer
from model import Customer
from time import time

bp = Blueprint("chat", __name__, url_prefix="/")

name_space = "/socketest"


@bp.route("/get_chatbot_answer", methods=["POST"])
def get_chatbot_answer():
    answer = ""

    if BOT_CHOICE == "WXBOT":
        message = request.form.get("msg")

        signature = session.get("signature")
        signature_timestamp = session.get("signature_timestamp")

        if not signature_timestamp or time() - signature_timestamp > 7200:
            userid = session.get("userid", f"guest_{time()}")
            signature = get_wxbot_signature(userid)
            session["signature"] = signature
            session["signature_timestamp"] = time()

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
