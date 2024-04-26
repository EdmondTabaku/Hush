from flask import Blueprint, request
from app.service.message import send_message, get_messages_for_client
from app.util.response import response

message_bp = Blueprint('message', __name__)


@message_bp.route('/', methods=['POST'])
def send_message_route():
    sender_id = request.json.get('sender_id')
    receiver_id = request.json.get('receiver_id')
    message = request.json.get('message')
    iv = request.json.get('iv')
    key = request.json.get('key')

    if not sender_id or not receiver_id or not message or not key or not iv:
        return response("", 'Invalid data', 400)

    new_message = send_message(sender_id, receiver_id, message, key, iv)
    if not new_message:
        return response("", 'Invalid receiver ID', 400)

    return response("", 'Message sent', 200)


@message_bp.route('/', methods=['GET'])
def get_messages_route():
    client_id = request.args.get('client_id')
    key = request.args.get('key')

    if not client_id or not key:
        return response("", 'Client id and key are required', 400)

    messages = get_messages_for_client(client_id, key)
    if messages is None:
        return response("", 'Invalid client id or key', 400)

    return response(messages, 'Messages retrieved', 200)
