"""Application models."""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class DBHelper(object):
    """Perform common SQLAlchemy tasks."""

    @staticmethod
    def add(item):
        """Add item to database."""
        db.session.add(item)
        db.session.commit()

    @staticmethod
    def delete(item):
        """Delete an item from the database."""
        db.session.delete(item)
        db.session.commit()


class User(UserMixin, db.Model):
    """User model, used for registration and login."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), default='user')
    password = db.Column(db.String(255), nullable=False)
    algorithms = db.relationship('Algorithm', backref='user', lazy=True)

    def set_password(self, password):
        """Set user password hash."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verify user's password."""
        return check_password_hash(self.password, password)

    @staticmethod
    def register(email, password):
        """Register a user."""
        prev_user = User.query.filter_by(email=email).first()
        if email and password and not prev_user:
            user = User(email=email, username=email)
            user.set_password(password)
            DBHelper.add(user)
            return user
        return None

    @staticmethod
    def get_user(email, password):
        """Find and authenticate a user."""
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return user
        return None

    def __repr__(self):
        """User representation."""
        return '<User {}>'.format(self.email)


class Algorithm(db.Model):
    """Algorithm model."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.String())
    sub_category = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    access = db.Column(db.String(100), default='public')

    def save(self):
        DBHelper.add(self)

    def delete(self):
        DBHelper.delete(self)

    @staticmethod
    def add(**kwargs):
        """Add item to database."""
        algorithm = Algorithm(**kwargs)
        DBHelper.add(algorithm)
        return algorithm

    @staticmethod
    def get(id_):
        return Algorithm.query.get(id_)

    def get_secure_attributes(self):
        """Return secure attributes as a Dict."""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'category_id': self.category_id,
            'sub_category': self.sub_category,
            'user_id': self.user_id,
            'access': self.access
        }


class Category(db.Model):
    """Category model."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    algorithms = db.relationship('Algorithm', backref='category', lazy=True)

    def save(self):
        return DBHelper.add(self)

    def delete(self):
        return DBHelper.delete(self)

    @staticmethod
    def get(id_):
        return Category.query.get(id_)

    @staticmethod
    def add(name):
        """Add item to database."""
        if Category.query.filter_by(name=name).first():
            return None
        category = Category(name=name)
        DBHelper.add(category)
        return category


@login_manager.user_loader
def load_user(user_id):
    """User loader for Flask-Login."""
    return User.query.get(user_id)
