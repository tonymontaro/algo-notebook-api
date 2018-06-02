"""Category routes."""

from flask import request, Blueprint, jsonify
from flask_login import login_required

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
        cat = Category.add(request.form.get('name'))
        if not cat:
            return jsonify({'message': 'Category already exists.'}), 409
        return jsonify({'id': cat.id, 'name': cat.name}), 201


@cat_bp.route('/<int:cat_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def category(cat_id):
    """Update, retrieve and delete a category."""
    missing_cat_res = jsonify({'message': 'Category does not exist.'}), 404
    if request.method == 'GET':
        cat = Category.get(cat_id)
        if not cat:
            return missing_cat_res
        return jsonify({'id': cat.id, 'name': cat.name}), 200

    if request.method == 'PUT':
        cat = Category.get(cat_id)
        if not cat:
            return missing_cat_res
        cat.name = request.form.get('name', cat.name)
        cat.save()
        return jsonify({'id': cat.id, 'name': cat.name}), 200

    if request.method == 'DELETE':
        cat = Category.get(cat_id)
        if not cat:
            return missing_cat_res
        cat.delete()
        return jsonify({'message': 'Category successfully deleted.'}), 200
