"""Module for testing the user registration and login."""

import unittest
import json

from app import create_app, db


class AlgorithmTestCase(unittest.TestCase):
    """Algorithm tests."""

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.user_data = {
            'email': 'montaro@gmail.com',
            'password': 'password'
        }
        self.cat1 = {'name': 'codility'}
        self.algo1 = {
            'title': 'Binary Sort',
            'content': 'print("hi")',
            'category': '1',
            'sub_category': 'sorting'
        }
        self.algo2 = {
            'title': 'Binary Search',
            'sub_category': 'searching'
        }
        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def login(self):
        """Login a user for other tests."""
        res = self.client.post('/users/register', data=self.user_data)
        assert res.status_code == 201
        login_res = self.client.post('/users/login', data=self.user_data)
        assert login_res.status_code == 200

    def create_category(self):
        """Create a category for other tests."""
        self.login()
        res = self.client.post('/categories', data=self.cat1)
        assert res.status_code == 201

    def test_create_algorithm(self):
        """Test the creation of an algorithm."""
        self.create_category()
        res = self.client.post('/users/algorithms', data=self.algo1)
        result = json.loads(res.data)
        assert res.status_code == 201
        assert result['title'] == 'Binary Sort'

    def create_algorithm(self):
        """Create an algorithm for other tests."""
        self.create_category()
        res = self.client.post('/users/algorithms', data=self.algo1)
        assert res.status_code == 201

    def test_get_algorithms(self):
        """Get algorithms belonging to a user"""
        self.create_category()
        res = self.client.post('/users/algorithms', data=self.algo1)
        assert res.status_code == 201

        res = self.client.get('/users/algorithms')
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

    def test_invalid_get_algorthm(self):
        """Return 404 if item does not exist."""
        self.login()
        res = self.client.get('/1')
        assert res.status_code == 404

    def test_update_algorithm(self):
        """Test that an algorithm can be updated."""
        self.create_algorithm()
        res = self.client.put('/1', data=self.algo2)
        assert res.status_code == 200
        result = json.loads(res.data)
        assert result['title'] == 'Binary Search'
        assert result['sub_category'] == 'searching'

    def test_invalid_get_algorithm(self):
        """Test that invalid algorithm id return 404."""
        res = self.client.put('/12', data=self.algo2)
        assert res.status_code == 404
        assert json.loads(res.data)['message'] == 'Algorithm does not exist.'

    def test_delete_algorithm(self):
        """Test that algorithms can be deleted."""
        self.create_algorithm()
        self.client.delete('/1')
        res = self.client.get('/1')
        assert res.status_code == 404

    def test_invalid_delete_algorithm(self):
        """Test for invalid user input."""
        res = self.client.delete('/22')
        assert res.status_code == 404

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
