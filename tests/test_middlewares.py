import pytest
from flask import Flask, session, g
from app.middlewares import session_message_middleware 

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = 'test'
    return app

def test_sets_error_message_correctly(app):
    with app.test_request_context('/some_route'):
        session['error'] = 'Error occurred'
        session_message_middleware()
        assert 'Error occurred' in g.message

def test_sets_success_message_correctly(app):
    with app.test_request_context('/some_route'):
        session['success'] = 'Success!'
        session_message_middleware()
        assert 'Success!' in g.message

def test_handles_when_there_are_no_messages(app):
    with app.test_request_context('/some_route'):
        session_message_middleware()
        assert g.message == ''
