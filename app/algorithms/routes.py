"""Sample API routes."""
from flask import Blueprint, jsonify, request

from app.models import Algorithm


algo_bp = Blueprint('algorithm', __name__)


@algo_bp.route('/')
def home():
    """Welcome page/message."""
    return jsonify({'message': 'Hello World!'}), 200


@algo_bp.route('/<algo_id>', methods=['GET', 'PUT', 'DELETE'])
def algorithm(algo_id):
    """Return an algorithm given the ID."""
    if request.method == 'GET':
        algo = Algorithm.get(algo_id)
        if not algo:
            return jsonify({'message': 'Algorithm does not exist.'}), 404
        return jsonify(algo.get_secure_attributes()), 200

    if request.method == 'PUT':
        req = request.form.get
        algo = Algorithm.get(algo_id)
        if not algo:
            return jsonify({'message': 'Algorithm does not exist.'}), 404
        attributes = [
            'id', 'title', 'content', 'category_id', 'sub_category', 'access']
        for attr in attributes:
            setattr(algo, attr, req(attr, getattr(algo, attr)))
        algo.save()
        return jsonify(algo.get_secure_attributes()), 200

    if request.method == 'DELETE':
        algo = Algorithm.get(algo_id)
        if not algo:
            return jsonify({'message': 'Algorithm does not exist.'}), 404
        title = algo.title
        algo.delete()
        return jsonify(
            {'message': "'{}' was deleted.".format(title)}), 200
