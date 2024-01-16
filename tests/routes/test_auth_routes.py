from flask import url_for
from flask_testing import TestCase
from flask_bcrypt import Bcrypt
from app import create_app
from unittest.mock import patch, MagicMock

bcrypt = Bcrypt()

class MockPrismaUser:
    def __init__(self):
        self.find_unique = MagicMock()
        self.create = MagicMock()

mock_prisma_user = MockPrismaUser()

class TestAuthRoutes(TestCase):
    def create_app(self):
        app = create_app()
        app.config['SERVER_NAME'] = 'localhost:5000'
        return app

    # Login Route
    @patch('app.config.Config.PRISMA.user', new=mock_prisma_user)
    def test_login_success_redirects(self):
        mock_prisma_user.find_unique.return_value = MagicMock(
            id=1,
            name='John Doe',
            email='johndoe@example.com',
            password=bcrypt.generate_password_hash('secret').decode('utf-8')
        )

        response = self.client.post('/login', data={
            'email': 'johndoe@example.com',
            'password': 'secret'
        })
        self.assertEqual(mock_prisma_user.find_unique.call_count, 1)
        self.assertEqual(response.location, url_for('user.user_posts', author_id=1))
        self.assertEqual(response.status_code, 302)

    def test_login_failure_redirects(self):
        response = self.client.post('/login', data={
            'email': 'invalid@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.location, '/login')
        self.assertEqual(response.status_code, 302)

    # Register Route
    @patch('app.config.Config.PRISMA.user', new=mock_prisma_user)
    def test_register_existing_email_redirects(self):
        existing_user = MagicMock(
            id=1,
            name='John Doe',
            email='johndoe@example.com',
            password=bcrypt.generate_password_hash('secret').decode('utf-8')
        )
        mock_prisma_user.find_unique.return_value = existing_user
         
        response = self.client.post('/register', data={
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'password': 'secret'
        })
        self.assertEqual(response.location, '/register')
        self.assertEqual(response.status_code, 302)


    @patch('app.config.Config.PRISMA.user', new=mock_prisma_user)
    def test_register_success_redirects(self):
        mock_prisma_user.find_unique.return_value = None
        mock_prisma_user.create.return_value = MagicMock(
            id=2,
            name='Jane Doe',
            email='janedoe@example.com'
        )
        response = self.client.post('/register', data={
            'name': 'Jane Doe',
            'email': 'janedoe@example.com',
            'password': 'secret'
        })
        self.assertEqual(response.location, '/login')
        self.assertEqual(response.status_code, 302)

# if __name__ == '__main__':
#     import unittest
#     unittest.main()
