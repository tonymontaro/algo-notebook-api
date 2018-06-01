"""Category routes."""

from flask import request, Blueprint, jsonify
from flask_login import login_required

from app.models import Category


cat_bp = Blueprint('category', __name__)


@cat_bp.route('', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def category():
    if request.method == 'GET':
        cats = [{'name': cat.name} for cat in Category.query.all()]
        return jsonify(cats)

    if request.method == 'POST':
        cat = Category.add(request.form.get('name'))
        return jsonify({'id': cat.id, 'name': cat.name}), 201
