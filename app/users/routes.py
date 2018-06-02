"""Authentication routes."""

from flask import request, Blueprint, jsonify
from flask_login import login_user, logout_user, login_required, current_user

from app.models import User, Algorithm


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register User route."""
    email = request.form.get('email')
    password = request.form.get('password')
    new_user = User.register(email, password)
    if new_user:
        return jsonify({'message': 'Registration successful.'}), 201
    return jsonify({'message': 'Invalid username or password.'}), 400


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login User route."""
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.get_user(email, password)
    if user:
        login_user(user)
        return jsonify({'message': 'Login successful.'}), 200
    return jsonify({'message': 'Invalid username or password.'}), 401


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout User route."""
    logout_user()
    return jsonify({'message': 'Logged out.'})


@auth_bp.route('/algorithms', methods=['GET'])
@auth_bp.route('/<int:user_id>/algorithms', methods=['GET'])
@login_required
def user_algorithms(user_id=None):
    """Get a user's algorithms or add one."""
    user_id = user_id or current_user.id
    user_algos = Algorithm.query.filter_by(user_id=user_id)
    user_algos = [algo.get_secure_attributes() for algo in user_algos]
    return jsonify(user_algos)
