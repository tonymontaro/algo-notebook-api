"""Module for testing the Categories."""

import os
import unittest

import pytest

from app import create_app, db
from tests.helpers import get_json, user1, admin, cat1, cat2


class CategoryTestCase(unittest.TestCase):
    """Category tests."""

    def setUp(self):
        self.route = '/categories'
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
        self.assertEqual(login_res.status_code, 200)

    def test_create_category(self):
        """Test for category creation."""
        self.login()
        res = self.client.post(self.route, data=cat1)
        result = get_json(res)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(result['name'], 'codility')

    def create_category(self):
        """Create a category for other tests."""
        self.login()
        res = self.client.post(self.route, data=cat1)
        assert res.status_code == 201

    def test_invalid_create_category(self):
        """Check invalid user inputs."""
        self.create_category()
        res = self.client.post(self.route, data=cat1)
        assert res.status_code == 409
        assert get_json(res)['message'] == 'Category already exists.'

    def test_get_categories(self):
        """Test that all categories can be retrieved."""
        self.login()
        add_cat_res = self.client.post(self.route, data=cat2)
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

    def test_update_category(self):
        """Test updating a category."""
        self.create_category()
        res = self.client.put(self.route + '/1', data=cat2)
        assert res.status_code == 200
        assert get_json(res)['name'] == 'hackerrank'

    def test_delete_category(self):
        """Test deleting a category."""
        self.create_category()
        res = self.client.delete(self.route + '/1')
        assert res.status_code == 200
        assert get_json(res)['message'] == "Category successfully deleted."

    def test_only_admin_can_create_update_or_delete_category(self):
        """Test that only the Admin can create, update or delete category."""
        res = self.client.post('/users/register', data=user1)
        self.assertEqual(res.status_code, 201)
        login_res = self.client.post('/users/login', data=user1)
        self.assertEqual(login_res.status_code, 200)

        res = self.client.post(self.route, data=cat1)
        assert res.status_code == 403
        assert get_json(res)['message'] == 'Unauthorized.'

        self.create_category()
        self.client.post('/users/logot')
        self.client.post('/users/login', data=user1)

        res = self.client.put(self.route + '/1', data=cat2)
        assert res.status_code == 403

        res = self.client.delete(self.route + '/1')
        assert res.status_code == 403

    def test_invalid_id_for_get_update_and_delete_of_category(self):
        """Return 404 if item does not exist."""
        self.login()
        res = self.client.get(self.route + '/22')
        assert res.status_code == 404
        assert get_json(res)['message'] == 'Category does not exist.'

        res = self.client.put(self.route + '/22', data=cat2)
        assert res.status_code == 404

        res = self.client.delete(self.route + '/22')
        assert res.status_code == 404

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    pytest.main()
