import unittest
from unittest.mock import patch, MagicMock
from app.utils.auth import authenticate, register_user, authorize


# TODO: Test Cases for authenticate

# ToDO: Test Cases for register_user

class TestAuthorize(unittest.TestCase):
    @patch('app.utils.auth.decode_token')
    def test_returns_null_if_no_token_provided(self, mock_decode_token):
        result = authorize(1, None)
        self.assertIsNone(result)

    @patch('app.utils.auth.decode_token')
    def test_returns_false_if_token_verification_fails(self, mock_decode_token):
        mock_decode_token.side_effect = Exception()
        result = authorize(1, 'invalidtoken')
        self.assertFalse(result)

    @patch('app.utils.auth.decode_token')
    def test_returns_false_if_user_id_does_not_match(self, mock_decode_token):
        mock_decode_token.return_value = {'sub': {'user': {'id': 2}}}
        result = authorize(1, 'validtoken')
        self.assertFalse(result)

    @patch('app.utils.auth.decode_token')
    def test_returns_true_if_user_id_matches_whats_in_the_token(self, mock_decode_token):
        mock_decode_token.return_value = {'sub': {'user': {'id': 1}}}
        result = authorize(1, 'validtoken')
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
