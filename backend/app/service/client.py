import string
import secrets
import time


class Client:
    def __init__(self, client_id):
        self.client_id = client_id
        self.created_at = time.time()
        self.key = generate_random_id(64)

    def __str__(self):
        return f'{self.client_id}'


CLIENTS = {}

"""
Create a new client
"""
def create_client():
    client_id = generate_random_id()

    # Uppercase the client id
    client_id = client_id.upper()

    while is_valid_client_id(client_id):
        client_id = generate_random_id()

    client = Client(client_id)
    CLIENTS[client_id] = client

    return client


"""
Get the client by id
"""
def get_client(client_id):
    client_id = client_id.upper()
    return CLIENTS.get(client_id)


"""
Check if the client id is valid
"""
def is_valid_client_id(client_id):
    client_id = client_id.upper()
    return client_id in CLIENTS


"""
Check if the client key is valid
"""
def is_valid_client_key(client_id, key):
    client_id = client_id.upper()
    client = get_client(client_id)
    if client is None:
        return False
    return client.key == key


"""
Remove the client id from the list
"""
def remove_client_id(client_id):
    client_id = client_id.upper()
    if is_valid_client_id(client_id):
        CLIENTS.pop(client_id)
        return True
    return False


"""
Generate a random id/key of a specific length. Default is 8
"""
def generate_random_id(length=8):
    # Define the possible characters: digits and letters
    characters = string.ascii_letters + string.digits
    random_id = ''.join(secrets.choice(characters) for _ in range(length))

    return random_id
