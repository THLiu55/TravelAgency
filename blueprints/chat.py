from flask import (
    Blueprint,
    request,
    render_template,
    g,
    redirect,
    url_for,
    session,
    current_app,
    jsonify,
)

from exts import socketio as io
from exts import db
from utils.bot import (
    BOT_CHOICE,
    BOT_CMD_RESP_DICT,
    get_wxbot_signature,
    get_wxbot_answer,
)
from utils.toys import get_fuzzed_room_name
from utils.decorators import login_required, staff_login_required
from model import Customer, Message
from time import time
from datetime import datetime
from flask_socketio import join_room, leave_room, send, emit
from sqlalchemy import desc
import os

bp = Blueprint("chat", __name__, url_prefix="/")

NAMESPACE = "/chat"
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")


### CHATBOT ROUTERS ###
@bp.route("/get_chatbot_answer", methods=["POST"])
def get_chatbot_answer():
    answer = ""

    if BOT_CHOICE == "WXBOT":
        message = request.form.get("msg")

        signature = session.get("signature")
        signature_timestamp = session.get("signature_timestamp")

        if not signature_timestamp or time() - signature_timestamp > 7200:
            userid = session.get("customer_id", f"guest_{time()}")
            signature = get_wxbot_signature(userid)
            session["signature"] = signature
            session["signature_timestamp"] = time()
            current_app.logger.info(
                "Generated new signature: "
                + signature
                + " for user with id "
                + str(userid)
            )

        answer = get_wxbot_answer(message, signature)

    return answer


@bp.route("/get_session_customer_info", methods=["GET"])
def get_session_customer_info():
    if session.get("customer_id"):
        customer = Customer.query.filter_by(id=session.get("customer_id")).first()
        if customer:
            return jsonify(
                {
                    "isLoggedIn": True,
                    "nickname": customer.nickname,
                    "cusId": customer.id,
                }
            )
    return jsonify({"isLoggedIn": False, "loginPageUrl": url_for("customer.login")})


@bp.route("/get_bot_cmd_resp_dict", methods=["GET"])
def get_bot_cmd_resp_dict():
    return jsonify(BOT_CMD_RESP_DICT)


@bp.route("/staff_load_chat_history/<customer_id>", methods=["GET"])
@staff_login_required
def staff_load_chat_history(customer_id):
    target_customer = Customer.query.filter_by(id=customer_id).first()
    to_return = [message.to_dict() for message in target_customer.messages]
    return jsonify(to_return)
    # return jsonify(get_history_by_cus_id(customer_id))


### END CHATBOT ROUTERS ###


### SOCKETIO EVENT HANDLERS ###
@io.on("connect", namespace=NAMESPACE)
def handle_connect():
    if session.get("staff_id"):
        print("admin connected.")
        io.emit(
            "message",
            {
                "sender": "system",
                "text": "Admin entered the chat room.",
            },
            broadcast=False,
            namespace=NAMESPACE,
        )
    elif session.get("customer_id"):
        customer = Customer.query.filter_by(id=session.get("customer_id")).first()
        if customer:
            print("customer " + customer.nickname + " connected.")
            room = get_fuzzed_room_name(customer.id)
            join_room(room)
            print("customer " + customer.nickname + " joined room: " + str(room))
            io.emit(
                "message",
                {
                    "sender": "system",
                    "text": "Welcome "
                    + customer.nickname
                    + " to the chat room, <a class='history-loader' onclick='requestForHistory()'>click here to load history</a>",
                },
                broadcast=False,
                namespace=NAMESPACE,
            )
        else:
            raise ConnectionRefusedError("User not found.")

    print("leaving default room " + request.sid)
    leave_room(request.sid)


@io.on("disconnect", namespace=NAMESPACE)
def handle_disconnect():
    db.session.commit()  # commit all messages sent by customer
    print("client disconnected.")


@io.on("join", namespace=NAMESPACE)
def handle_join(data):
    if session.get("staff_id"):
        customer_id = data["target_customer_id"]
        room = get_fuzzed_room_name(customer_id)
        print("admin joining room: " + str(room) + " for customer " + str(customer_id))
        join_room(room)
        io.send(
            data={"sender": "system", "text": "admin joined the conversation."},
            namespace=NAMESPACE,
            to=room,
        )
    elif session.get("customer_id"):
        customer_id = session.get("customer_id")
        customer = Customer.query.filter_by(id=customer_id).first()
        room = get_fuzzed_room_name(customer.id)
        print("customer " + customer.nickname + " client joining room: " + str(room))
        join_room(room)
        io.send(
            data={"text": customer.nickname + " joined room " + str(room)},
            namespace=NAMESPACE,
            to=room,
        )


@io.on("leave", namespace=NAMESPACE)
def handle_leave(data):
    db.session.commit()  # commit all messages sent by customer
    customer_id = data["target_customer_id"]
    room = get_fuzzed_room_name(customer_id)
    print("leaving room: " + str(room))
    leave_room(room)
    io.send(
        data={"text": "left room " + str(room) + " for customer " + customer_id},
        namespace=NAMESPACE,
        to=room,
    )


@io.on("message", namespace=NAMESPACE)
def handle_message(data):
    sender_name = data["sender"]
    msg_text = data["text"]
    sending_data = {"sender": sender_name, "text": msg_text}
    if sender_name == "system":
        io.emit("message", sending_data, broadcast=False, namespace=NAMESPACE)
    elif sender_name == ADMIN_USERNAME:
        target_customer_id = data["target_customer_id"]
        target_customer = Customer.query.filter_by(id=target_customer_id).first()
        target_room = get_fuzzed_room_name(target_customer_id)
        print(
            sender_name
            + " sending message: "
            + msg_text
            + " to room: "
            + str(target_room)
        )
        io.send(data=sending_data, namespace=NAMESPACE, to=target_room)
        new_message = Message(
            customerID=target_customer_id,
            sentTime=datetime.now(),
            content=msg_text,
            isPic=False,
            isByCustomer=False,
        )
        target_customer.amount_unread_msgs += 1
        db.session.add(new_message)
        db.session.commit()
    else:
        # theoretically, this is for customer
        customer_id = session.get("customer_id")
        customer = Customer.query.filter_by(id=customer_id).first()
        if customer.nickname != sender_name:
            raise ConnectionRefusedError("User not found.")
        room = get_fuzzed_room_name(customer.id)
        print(sender_name + " sending message: " + msg_text + " to room: " + str(room))
        io.send(data=sending_data, namespace=NAMESPACE, to=room)
        new_message = Message(
            customerID=customer_id,
            isPic=False,
            content=msg_text,
            sentTime=datetime.now(),
            isByCustomer=True,
        )
        customer.amount_unread_msgs += 1
        db.session.add(new_message)
        db.session.commit()


@io.on("req4history", namespace=NAMESPACE)
@login_required
def handle_req4history(data):
    """For customer to request for history"""
    cusId = data["cusId"]
    room = get_fuzzed_room_name(cusId)
    messages = get_history_by_cus_id(cusId)
    for message in messages:
        if message.isByCustomer:  # TODO: Pic related logic
            sender = message.customer.nickname
        else:
            sender = ADMIN_USERNAME
        sending_data = {
            "isHistory": True,
            "sentTime": message.sentTime.strftime("%Y-%m-%d %H:%M:%S"),
            "sender": sender,
            "text": message.content,
        }
        io.send(data=sending_data, namespace=NAMESPACE, to=room)


@io.on("read", namespace=NAMESPACE)
@staff_login_required
def handle_read(data):
    """This is for admin to mark a customer's message as read"""
    print("marking message as read")
    cusId = data["cusId"]
    customer = Customer.query.filter_by(id=cusId).first()
    customer.amount_unread_msgs = 0
    db.session.commit()


### END SOCKETIO EVENT HANDLERS ###

# TODO: refactor socketio.emit, socketio.send to emit, send in the future


### UTILS ###
def get_history_by_cus_id(customer_id):
    messages = (
        Message.query.filter_by(customerID=customer_id)
        .order_by(desc(Message.sentTime))
        .limit(20)
        .all()[::-1]
    )  # TODO: dynamic limit refactor
    return messages