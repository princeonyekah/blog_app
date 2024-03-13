"""Routes for authentication."""
from os import environ
from flask import (
    Blueprint,
    request,
    redirect,
    render_template,
    session,
    make_response,
    url_for,
)
from flask_jwt_extended import create_access_token
import jwt
from app.utils.auth import authenticate, register_user
from app.config import Config
from datetime import timedelta
from markupsafe import Markup

prisma = Config.PRISMA

SECRET_KEY = environ.get("SECRET_KEY", "secret-key")


auth_routes = Blueprint("auth", __name__)


@auth_routes.route("/login", methods=["GET"])
def login():
    """Show login page."""
    access_token = request.cookies.get("access_token")
    try:
        if access_token:
            # Decode the access token to extract author_id
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256'])
            author_id = payload.get('sub', {}).get('user', {}).get('id')
            author = prisma.user.find_unique(where={"id": author_id})
            posts = prisma.post.find_many(where={"authorId": author_id},
                                            order={"createdAt": "desc"})
            # Truncate post content if it's longer than 40 characters
            for post in posts:
                post.content = Markup(post.content)
                if len(post.content) > 40:
                    post.content = post.content[:40] + "..."
            return render_template("myblogs.html", posts=posts, author=author, showLogout=True)
        else:
            return render_template("login.html", signIn = True, showLogout=False)
    except jwt.ExpiredSignatureError:
        # Handle expired token error
        return render_template("login.html", signIn=True, showLogout=False, error="Token expired.")
    except jwt.InvalidTokenError:
        # Handle invalid token error
        return render_template("login.html", signIn=True, showLogout=False, error="Invalid token.")

@auth_routes.route("/login", methods=["POST"])
def login_post():
    """Login a user."""
    user = authenticate(request.form["email"], request.form["password"])
    if user:
        session.clear()
        session[
            "success"
        ] = f'Authenticated as {user.name} click to <a href="/logout">logout</a>.'
        token = create_access_token(
            identity={"user": {"id": user.id}}
        )
        resp = make_response(redirect(url_for("user.user_posts", author_id=user.id, showLogout = True)))
        resp.set_cookie("access_token", token, httponly=True, max_age=86400)
        return resp
    session["error"] = "Authentication failed, please check your email and password."
    return redirect("/login")


@auth_routes.route("/logout", methods=["GET"])
def logout():
    """Logout a user."""
    session.clear()
    resp = make_response(redirect("/"))
    resp.delete_cookie("access_token")
    return resp


@auth_routes.route("/register", methods=["GET"])
def register():
    """Show register page."""
    return render_template("register.html", showLogout=False)


@auth_routes.route("/register", methods=["POST"])
def register_post():
    """Register a new user."""
    email = request.form["email"]
    existing_user = prisma.user.find_unique(where={"email": email})

    if existing_user:
        session["error"] = "Registration failed, email already exists."
        return redirect("/register")
    register_user(request.form["name"], email, request.form["password"])
    session["error"] = "Registration Successful, please login."
    return redirect("/login")

