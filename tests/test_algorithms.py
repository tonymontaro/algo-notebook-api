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
        res = self.client.post('/user/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        login_res = self.client.post('/user/login', data=self.user_data)
        self.assertEqual(login_res.status_code, 200)

    def create_category(self):
        res = self.client.post('/categories', data=self.cat1)
        self.assertEqual(res.status_code, 201)

    def test_create_algorithm(self):
        """Test the creation of an algorithm."""
        self.login()
        self.create_category()
        res = self.client.post('/user/algorithms', data=self.algo1)
        result = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(result['title'], 'Binary Sort')

    def create_algorithm(self):
        """Create an algorithm for testing."""
        self.login()
        self.create_category()
        res = self.client.post('/user/algorithms', data=self.algo1)
        self.assertEqual(res.status_code, 201)

    def test_get_algorithms(self):
        """Get algorithms belonging to a user"""
        self.login()
        self.create_category()
        res = self.client.post('/user/algorithms', data=self.algo1)
        self.assertEqual(res.status_code, 201)

        res = self.client.get('/user/algorithms')
        self.assertEqual(res.status_code, 200)
        result = json.loads(res.data)
        self.assertEqual(result[0]['title'], 'Binary Sort')

    def test_get_algorithm(self):
        """Get an algorithm."""
        self.create_algorithm()
        res = self.client.get('/1')
        self.assertEqual(res.status_code, 200)
        result = json.loads(res.data)
        self.assertEqual(result['title'], 'Binary Sort')

    def test_update_algorithm(self):
        """Update an algorithm."""
        self.create_algorithm()
        res = self.client.put('/1', data=self.algo2)
        self.assertEqual(res.status_code, 200)
        result = json.loads(res.data)
        self.assertEqual(result['title'], 'Binary Search')
        self.assertEqual(result['sub_category'], 'searching')

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
