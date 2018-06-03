"""Module for testing the user registration and login."""

import os
import unittest
import json

from app import create_app, db
from tests.helpers import user1, admin


class AuthTestCase(unittest.TestCase):
    """User userentication tests."""

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_user_registration(self):
        """Test for successful user registration."""
        res = self.client.post('/users/register', data=user1)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Registration successful.")
        self.assertEqual(res.status_code, 201)

    def register(self):
        """Register user."""
        res = self.client.post('/users/register', data=user1)
        self.assertEqual(res.status_code, 201)

    def test_invalid_user_registration(self):
        """Test for registration when the user already exists."""
        res = self.client.post('/users/register', data=user1)
        self.assertEqual(res.status_code, 201)
        second_res = self.client.post('/users/register', data=user1)
        self.assertEqual(second_res.status_code, 400)
        result = json.loads(second_res.data.decode())
        self.assertEqual(result['message'], "Invalid username or password.")

    def test_user_login(self):
        """Test for user login."""
        self.register()
        login_res = self.client.post('/users/login', data=user1)
        result = json.loads(login_res.data)
        self.assertEqual(result['message'], "Login successful.")
        self.assertEqual(login_res.status_code, 200)

    def test_user_invalid_login(self):
        """Test for invalid user login."""
        self.register()
        wrong_pass_user = {
            'email': 'montaro@gmail.com',
            'password': 'wrong-password'
        }
        login_res = self.client.post('/users/login', data=wrong_pass_user)
        result = json.loads(login_res.data)
        self.assertEqual(result['message'], "Invalid username or password.")
        self.assertEqual(login_res.status_code, 401)

    def login(self):
        """Login user."""
        self.register()
        login_res = self.client.post('/users/login', data=user1)
        self.assertEqual(login_res.status_code, 200)

    def test_user_logout(self):
        """Test for user login."""
        self.login()
        logout_res = self.client.post('/users/logout')
        result = json.loads(logout_res.data)
        self.assertEqual(result['message'], 'Logged out.')
        self.assertEqual(logout_res.status_code, 200)

    def test_seeding_the_db_with_admnin_details(self):
        """Seed the database."""
        os.environ['ADMIN_EMAIL'] = admin['email']
        os.environ['ADMIN_PASSWORD'] = admin['password']
        client = create_app("testing").test_client()

        login_res = client.post('/users/login', data=admin)
        assert login_res.status_code == 200
        assert json.loads(login_res.data)['message'] == "Login successful."

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
