"""Module for testing Algorithm routes."""

import os
import unittest
import json

import pytest

from app import create_app, db
from tests.helpers import admin, user2, algo1, algo2, cat1, get_json


class AlgorithmTestCase(unittest.TestCase):
    """Algorithm tests."""

    def setUp(self):
        os.environ['ADMIN_EMAIL'] = admin['email']
        os.environ['ADMIN_PASSWORD'] = admin['password']
        self.app = create_app("testing")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def login(self):
        """Login a user for other tests."""
        login_res = self.client.post('/users/login', data=admin)
        assert login_res.status_code == 200

    def logout(self):
        """Logout a user."""
        logout = self.client.post('/users/logout')
        assert logout.status_code == 200

    def create_category(self):
        """Create a category for other tests."""
        self.login()
        res = self.client.post('/categories', data=cat1)
        assert res.status_code == 201

    def test_create_algorithm(self):
        """Test the creation of an algorithm."""
        self.create_category()
        res = self.client.post('/', data=algo1)
        result = json.loads(res.data)
        assert res.status_code == 201
        assert result['title'] == 'Binary Sort'

    def test_login_required_to_create_delete_or_update_algorithm(self):
        """Ensure that the user is logged before creating an algorithm."""
        res = self.client.post('/', data=algo1)
        assert res.status_code == 401
        assert get_json(res)['message'] == 'Login required.'

        self.create_algorithm()
        self.logout()

        res = self.client.put('/1', data=algo1)
        assert res.status_code == 401

        res = self.client.delete('/1', data=algo1)
        assert res.status_code == 401

    def test_missing_fields_for_create_algorithm(self):
        """Test for errors related to creating an algorithm."""
        self.create_category()
        missing_title = {
            'content': 'print("hi")',
            'category': '1',
            'sub_category': 'sorting'
        }
        res = self.client.post('/', data=missing_title)
        assert get_json(res)['message'] == 'Invalid title or category id.'

        invalid_category = {
            'title': 'Binary Sort',
            'content': 'print("hi")',
            'category': 'abcd',
            'sub_category': 'sorting'
        }
        res = self.client.post('/', data=invalid_category)
        assert get_json(res)['message'] == 'Invalid title or category id.'

    def create_algorithm(self):
        """Create an algorithm for other tests."""
        self.create_category()
        res = self.client.post('/', data=algo1)
        assert res.status_code == 201

    def test_get_user_algorithms(self):
        """Get algorithms belonging to a user"""
        self.create_algorithm()
        res = self.client.get('/users/algorithms')
        assert res.status_code == 200
        result = json.loads(res.data)
        assert result[0]['title'] == 'Binary Sort'

    def test_get_public_algorithms(self):
        """Get algorithms belonging to a user"""
        self.create_algorithm()
        res = self.client.get('/')
        assert res.status_code == 200
        result = json.loads(res.data)
        assert result[0]['title'] == 'Binary Sort'

    def test_get_algorithm(self):
        """Get an algorithm."""
        self.create_algorithm()
        res = self.client.get('/1')
        assert res.status_code == 200
        result = json.loads(res.data)
        assert result['title'] == 'Binary Sort'

    def test_update_algorithm(self):
        """Test that an algorithm can be updated."""
        self.create_algorithm()
        res = self.client.put('/1', data=algo2)
        assert res.status_code == 200
        result = json.loads(res.data)
        assert result['title'] == 'Binary Search'
        assert result['sub_category'] == 'searching'

    def test_delete_algorithm(self):
        """Test that algorithms can be deleted."""
        self.create_algorithm()
        self.client.delete('/1')
        res = self.client.get('/1')
        assert res.status_code == 404

    def test_invalid_id_for_get_put_and_delete(self):
        """Return 404 if item does not exist."""
        self.login()
        res = self.client.get('/22')
        assert res.status_code == 404
        assert json.loads(res.data)['message'] == 'Algorithm does not exist.'

        res = self.client.put('/200', data=algo2)
        assert res.status_code == 404

        res = self.client.delete('/22')
        assert res.status_code == 404

    def test_algorithm_author_can_update_or_delete(self):
        """Test only the owner can update and delete an algorithm."""
        self.create_algorithm()
        self.logout()
        res = self.client.post('/users/register', data=user2)
        assert res.status_code == 201
        login_res = self.client.post('/users/login', data=user2)
        assert login_res.status_code == 200

        update = self.client.put('/1', data=algo2)
        assert update.status_code == 403
        assert get_json(update)['message'] == 'Unauthorized.'

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    pytest.main()
