import unittest
from flask import Flask
from EGPT import create_app, db
from EGPT.models import User

class TestUserManagement(unittest.TestCase):

    def setUp(self):
        self.app = create_app('test_config')
        self.client = self.app.test_client()
        
        # Context for testing
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_new_user(self):
        # Test user registration functionality
        response = self.client.post('/register', data={
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'password',
            'confirm_password': 'password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your account has been created! You are now able to log in', response.data)

        # Verify user is added to the database
        with self.app.app_context():
            user = User.query.filter_by(username='johndoe').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.email, 'johndoe@example.com')

    def test_login_and_logout(self):
        # Test user login and logout functionality
        response = self.client.post('/login', data={
            'email': 'johndoe@example.com',
            'password': 'password',
            'remember': False
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged in successfully', response.data)

        # Test logout
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been logged out', response.data)

if __name__ == '__main__':
    unittest.main()
