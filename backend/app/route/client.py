from flask import Blueprint
from app.service.client import create_client
from app.util.response import response


client_bp = Blueprint('client', __name__)


@client_bp.route('/', methods=['POST'])
def create_client_route():
    client = create_client()
    return response(client.__dict__, 'Client created', 200)