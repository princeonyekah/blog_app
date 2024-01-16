from flask import url_for
from flask_testing import TestCase
from flask_bcrypt import Bcrypt
from app import create_app
from unittest.mock import patch, MagicMock

bcrypt = Bcrypt()

class MockPrismaPost:
    def __init__(self):
        self.find_unique = MagicMock()
        self.create = MagicMock()

mock_prisma_post = MockPrismaPost()

data = {
  'authorId': 1,
  'title': 'Test Title',
  'content': 'Test Content',
  'authorEmail': 'test@example.com',
}

class TestPostRoutes(TestCase):
    def create_app(self):
        app = create_app()
        app.config['SERVER_NAME'] = 'localhost:5000'
        return app

    # Post Route
    @patch('app.config.Config.PRISMA.post', new=mock_prisma_post)
    @patch('app.routes.post_routes.authorize', return_value = True)
    def test_create_valid_post_and_redirect(self, mock_authorize):
        mock_prisma_post.create.return_value = MagicMock(
            id=1
        )
        response = self.client.post(url_for('post.create_post'), data=data)
        self.assertEqual(mock_authorize.call_count, 1)
        self.assertEqual(mock_prisma_post.create.call_count, 1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/user/1/posts')

    @patch('app.routes.post_routes.authorize', return_value = False)
    def test_fail_if_not_authorized(self, mock_authorize):
        response = self.client.post(url_for('post.create_post'), data=data)
        self.assertEqual(mock_authorize.call_count, 1)
        self.assertEqual(response.status_code, 403)
    
    @patch('app.routes.post_routes.authorize', return_value = True)
    def test_fail_and_redirect_if_invalid_post(self, mock_authorize):
        response = self.client.post(url_for('post.create_post'), data={'title': "Test Tile", 'authorEmail': "test@example.com"})
        self.assertEqual(response.status_code, 400)

   