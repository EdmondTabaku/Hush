from flask import Blueprint
from app.service.client import create_client, is_valid_client_id, is_valid_client_key
from app.util.response import response


client_bp = Blueprint('client', __name__)


@client_bp.route('/', methods=['GET'])
def create_client_route():
    client = create_client()
    return response(client.__dict__, 'Client created', 200)


@client_bp.route('/<client_id>/<key>', methods=['GET'])
def is_valid_client_id_route(client_id, key):
    is_valid_client = is_valid_client_id(client_id)
    is_valid_key = is_valid_client_key(client_id, key)

    if is_valid_client and is_valid_key and is_valid_client is True and is_valid_key is True:
        return response({"is_valid": True}, 'Client is valid', 200)

    return response({"is_valid": False}, 'Client is invalid', 400)
