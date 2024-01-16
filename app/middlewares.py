"""This module contains all the middlewares used in the application."""
from flask import session, g
from flask_session import Session
from .config import Config


def setup_middlewares(app):
    """Setup all the middlewares used in the application."""
    app.config["SECRET_KEY"] = Config.SECRET_KEY
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    app.before_request(session_message_middleware)


def session_message_middleware():
    """Middleware to handle session messages."""
    err = session.pop("error", None)
    msg = session.pop("success", None)
    g.message = ""
    if err:
        g.message = f'<div class="alert alert-warning" role="alert">{err}</div>'
    if msg:
        g.message = f'<div class="alert alert-success" role="alert">{msg}</div>'
