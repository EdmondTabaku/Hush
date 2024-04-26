import time
from app.service.client import is_valid_client_id, get_client
from app import logger

class Message:
    def __init__(self, sender_id, receiver_id, message):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.message = message
        self.created_at = time.time()

    def __str__(self):
        return f'{self.message}'


MESSAGES = {}

"""
Send message to client
"""
def send_message(sender_id, receiver_id, message, key):
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

    new_message = Message(sender_id, receiver_id, message)
    MESSAGES[receiver_id] = MESSAGES.get(receiver_id, []) + [new_message]
    logger.info(f'Message sent to client {receiver_id}')

    return new_message


"""
Get messages for a specific client
"""
def get_messages_for_client(client_id, key):
    if not is_valid_client_id(client_id):
        logger.error(f'Invalid client id: {client_id}')
        return None

    client = get_client(client_id)
    if client.key != key:
        logger.error(f'Invalid client key: {key}')
        return None

    messages = MESSAGES.get(client_id, [])
    logger.info(f'Messages retrieved for client {client_id}')

    messages_json = []
    for message in messages:
        messages_json.append(message.__dict__)

    return messages_json


