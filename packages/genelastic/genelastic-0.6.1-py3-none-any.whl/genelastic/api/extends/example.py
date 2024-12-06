# pylint: disable=missing-module-docstring
from flask import jsonify, Response


def ping_2() -> Response:
    """Test route to verify that the server is online."""
    return jsonify({'message': 'pong_2'})
