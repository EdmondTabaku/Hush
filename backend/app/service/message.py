import time
import uuid

from app.service.client import is_valid_client_id, get_client
from app import logger

class Message:
    def __init__(self, sender_id, receiver_id, message, iv):
        self.id = uuid.uuid4().hex
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.message = message
        self.iv = iv
        self.created_at = time.time()

    def __str__(self):
        return f'{self.message}'


RECEIVER_MESSAGES = {}
SENDER_MESSAGES = {}

"""
Send message to client
"""
def send_message(sender_id, receiver_id, message, key, iv):
    sender_id = sender_id.upper()
    receiver_id = receiver_id.upper()

    if not is_valid_client_id(sender_id):
        logger.error(f'Invalid sender id: {sender_id}')
        return None

    if not is_valid_client_id(receiver_id):
        logger.error(f'Invalid receiver id: {receiver_id}')
        return None

    client = get_client(sender_id)
    if client.key != key:
        logger.error(f'Invalid sender key: {key}')
        return None

    new_message = Message(sender_id, receiver_id, message, iv)
    RECEIVER_MESSAGES[receiver_id] = RECEIVER_MESSAGES.get(receiver_id, []) + [new_message]
    SENDER_MESSAGES[sender_id] = SENDER_MESSAGES.get(sender_id, []) + [new_message]
    logger.info(f'Message sent to client {receiver_id}')

    return new_message


"""
Get messages for a specific client
"""
def get_messages_for_client(client_id, key):
    client_id = client_id.upper()
    if not is_valid_client_id(client_id):
        logger.error(f'Invalid client id: {client_id}')
        return None

    client = get_client(client_id)
    if client.key != key:
        logger.error(f'Invalid client key: {key}')
        return None

    receiver_messages = RECEIVER_MESSAGES.get(client_id, [])
    sender_messages = SENDER_MESSAGES.get(client_id, [])

    messages = receiver_messages + sender_messages

    # Filter out and delete messages that are older than 24 hours
    current_time = time.time()
    messages = [message for message in messages if current_time - message.created_at < 86400]

    # Filter out the duplicate messages with the same id
    messages = list({message.id: message for message in messages}.values())

    messages.sort(key=lambda x: x.created_at)

    messages_json = []
    for message in messages:
        messages_json.append(message.__dict__)

    return messages_json


