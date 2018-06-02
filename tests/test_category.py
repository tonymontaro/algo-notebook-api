"""Module for testing the user registration and login."""
import unittest
import json

import pytest

from app import create_app, db


def get_json(res):
    """Return json response as a dictionary or list."""
    return json.loads(res.data)


class CategoryTestCase(unittest.TestCase):
    """User userentication tests."""

    def setUp(self):
        self.route = '/categories'
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
        """Login a user for other tests."""
        res = self.client.post('/users/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        login_res = self.client.post('/users/login', data=self.user_data)
        self.assertEqual(login_res.status_code, 200)

    def test_create_category(self):
        """Test for category creation."""
        self.login()
        res = self.client.post(self.route, data=self.cat1)
        result = get_json(res)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(result['name'], 'codility')

    def create_category(self):
        """Create a category for other tests."""
        self.login()
        res = self.client.post(self.route, data=self.cat1)
        assert res.status_code == 201

    def test_invalid_create_category(self):
        """Check invalid user inputs."""
        self.create_category()
        res = self.client.post(self.route, data=self.cat1)
        assert res.status_code == 409
        assert get_json(res)['message'] == 'Category already exists.'

    def test_get_categories(self):
        """Test that all categories can be retrieved."""
        self.login()
        add_cat_res = self.client.post(self.route, data=self.cat2)
        self.assertEqual(add_cat_res.status_code, 201)

        res = self.client.get(self.route)
        result = get_json(res)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(result[0]['name'], 'hackerrank')

    def test_get_category(self):
        """Test that a category can be retrieved."""
        self.create_category()
        res = self.client.get(self.route + '/1')
        assert res.status_code == 200
        assert get_json(res)['name'] == 'codility'

    def test_invalid_get_category(self):
        """Test for invalid inputs to get-category."""
        self.login()
        res = self.client.get(self.route + '/22')
        assert res.status_code == 404
        assert get_json(res)['message'] == 'Category does not exist.'

    def test_update_category(self):
        """Test updating a category."""
        self.create_category()
        res = self.client.put(self.route + '/1', data=self.cat2)
        assert res.status_code == 200
        assert get_json(res)['name'] == 'hackerrank'

    def test_invalid_category_update(self):
        """Check for category update errors."""
        self.login()
        res = self.client.put(self.route + '/22', data=self.cat2)
        assert res.status_code == 404

    def test_delete_category(self):
        """Test deleting a category."""
        self.create_category()
        res = self.client.delete(self.route + '/1')
        assert res.status_code == 200
        assert get_json(res)['message'] == "Category successfully deleted."

    def test_invalid_delete_category(self):
        """Test for category delete errors."""
        self.login()
        res = self.client.delete(self.route + '/22')
        assert res.status_code == 404

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    pytest.main()
