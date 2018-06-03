"""Category routes."""

from flask import request, Blueprint, jsonify
from flask_login import login_required, current_user

from app.models import Category


cat_bp = Blueprint('category', __name__)


@cat_bp.route('', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def categories():
    """Create and retrieve categories."""
    if request.method == 'GET':
        cats = [
            {'id': cat.id, 'name': cat.name} for cat in Category.query.all()]
        return jsonify(cats)

    if request.method == 'POST':
        if current_user.role != 'admin':
            return jsonify({'message': 'Unauthorized.'}), 403
        cat = Category.add(request.form.get('name'))
        if not cat:
            return jsonify({'message': 'Category already exists.'}), 409
        return jsonify({'id': cat.id, 'name': cat.name}), 201


@cat_bp.route('/<int:cat_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def category(cat_id):
    """Update, retrieve and delete a category."""
    cat = Category.get(cat_id)
    if not cat:
        return jsonify({'message': 'Category does not exist.'}), 404

    if request.method == 'GET':
        return jsonify({'id': cat.id, 'name': cat.name}), 200
    elif current_user.role != 'admin':
        return jsonify({'message': 'Unauthorized.'}), 403

    if request.method == 'PUT':
        cat.name = request.form.get('name', cat.name)
        cat.save()
        return jsonify({'id': cat.id, 'name': cat.name}), 200
    elif request.method == 'DELETE':
        cat.delete()
        return jsonify({'message': 'Category successfully deleted.'}), 200
