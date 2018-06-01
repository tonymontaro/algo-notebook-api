"""Sample API routes."""
from flask import Blueprint, jsonify, request

from app.models import Algorithm


algo_bp = Blueprint('algorithm', __name__)


@algo_bp.route('/')
def home():
    """Welcome page/message."""
    return jsonify({'message': 'Hello World!'})


@algo_bp.route('/<algo_id>', methods=['GET', 'PUT', 'DELETE'])
def algorithm(algo_id):
    """Return an algorithm given the ID."""
    if request.method == 'GET':
        algo = Algorithm.get(algo_id)
        return jsonify(algo.get_secure_attributes())

    if request.method == 'PUT':
        return jsonify({'m': 'ready'})
