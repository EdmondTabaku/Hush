from flask import jsonify


def response(data, message, status):
    return jsonify({'data': data, 'message': message, 'status': status})