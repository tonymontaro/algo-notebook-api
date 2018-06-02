"""Sample API routes."""
from flask import Blueprint, jsonify, request
from flask_login import current_user

from app.models import Algorithm


algo_bp = Blueprint('algorithm', __name__)


@algo_bp.route('/', methods=['GET', 'POST'])
def home():
    """Retrieve public algorithms or create an algorithm."""
    if request.method == 'GET':
        algos = Algorithm.query.all()
        algos = [algo.get_secure_attributes() for algo in algos]
        return jsonify(algos)

    if request.method == 'POST':
        if not current_user.is_authenticated:
            return jsonify({'message': 'Login required.'}), 401
        req = request.form.get
        try:
            algo = Algorithm.add(title=req('title'),
                                 content=req('content'),
                                 category_id=int(req('category')),
                                 sub_category=req('sub_category'),
                                 user_id=current_user.id)
        except:
            return jsonify({'message': 'Invalid title or category id.'})
        return jsonify(algo.get_secure_attributes()), 201


@algo_bp.route('/<int:algo_id>', methods=['GET', 'PUT', 'DELETE'])
def algorithm(algo_id):
    """Return an algorithm given the ID."""
    algo = Algorithm.get(algo_id)
    if not algo:
        return jsonify({'message': 'Algorithm does not exist.'}), 404

    if request.method == 'GET':
        return jsonify(algo.get_secure_attributes()), 200
    elif request.method == 'PUT':
        req = request.form.get
        attributes = [
            'id', 'title', 'content', 'category_id', 'sub_category', 'access']
        for attr in attributes:
            setattr(algo, attr, req(attr, getattr(algo, attr)))
        algo.save()
        return jsonify(algo.get_secure_attributes()), 200
    elif request.method == 'DELETE':
        title = algo.title
        algo.delete()
        return jsonify(
            {'message': "'{}' was deleted.".format(title)}), 200
