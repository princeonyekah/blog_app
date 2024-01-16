from datetime import datetime
from flask import url_for
from flask_testing import TestCase
from app import create_app
from unittest.mock import patch, MagicMock

class MockPrismaUser:
    def __init__(self):
        self.find_unique = MagicMock()

class MockPrismaPost:
    def __init__(self):
        self.find_many = MagicMock()

mock_prisma_user = MockPrismaUser()
mock_prisma_post = MockPrismaPost()

author = MagicMock()
author.id = 1
author.name = "John Doe"

posts =  [ 
    MagicMock(
        authorId = 1,
        title = "Test Title",
        content = "Test Content",
        authorEmail = "test@example.com",
        createdAt = datetime.strptime('2021-08-01T00:00:00.000Z', '%Y-%m-%dT%H:%M:%S.%fZ')
    )
]

class TestUserRoutes(TestCase):
    def create_app(self):
        app = create_app()
        app.config['SERVER_NAME'] = 'localhost:5000'
        return app

    # user/id/posts Route
    @patch('app.config.Config.PRISMA.post', new=mock_prisma_post)
    @patch('app.config.Config.PRISMA.user', new=mock_prisma_user)
    @patch('app.routes.user_routes.authorize', return_value = True)
    def test_return_all_post_for_authorized_user(self, mock_authorize):

        mock_prisma_user.find_unique.return_value = author
        mock_prisma_post.find_many.return_value = posts
        response = self.client.get(url_for('user.user_posts', author_id=author.id))
        self.assertEqual(mock_authorize.call_count, 1)
        self.assertEqual(mock_prisma_post.find_many.call_count, 1)
        self.assertEqual(mock_prisma_user.find_unique.call_count, 1)
        self.assertEqual(response.status_code, 200)
        self.assertIn(author.name, response.text)
        self.assertIn(posts[0].title, response.text)
        self.assertIn(posts[0].content, response.text)
        self.assertIn(posts[0].createdAt.strftime('%Y-%m-%d'), response.text)

    @patch('app.routes.user_routes.authorize', return_value = False)
    def test_return_403_for_unauthorized_user(self, mock_authorize):
        response = self.client.get(url_for('user.user_posts', author_id=author.id))
        self.assertEqual(mock_authorize.call_count, 1)
        self.assertEqual(response.status_code, 403)

   