"""Module for testing the user registration and login."""
import unittest
import json

from app import create_app, db


class CategoryTestCase(unittest.TestCase):
    """User userentication tests."""

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.user_data = {
            'email': 'montaro@gmail.com',
            'password': 'password'
        }
        self.cat1 = {'name': 'codility'}
        self.cat2 = {'name': 'hackerrank'}
        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def login(self):
        res = self.client.post('/user/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        login_res = self.client.post('/user/login', data=self.user_data)
        self.assertEqual(login_res.status_code, 200)

    def test_create_category(self):
        """Test for category creation."""
        self.login()
        res = self.client.post('/categories', data=self.cat1)
        result = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(result['name'], 'codility')

    def test_get_categories(self):
        """Test get categories route."""
        self.login()
        add_cat_res = self.client.post('/categories', data=self.cat2)
        self.assertEqual(add_cat_res.status_code, 201)

        res = self.client.get('/categories')
        result = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(result[0]['name'], 'hackerrank')

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
