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

# Initialize Prisma Database connection
prisma = Config.PRISMA

# Get the secret key from environment variables or use a default value
SECRET_KEY = environ.get("SECRET_KEY", "secret-key")

# Create a blueprint for authentication routes
auth_routes = Blueprint("auth", __name__)

@auth_routes.route("/login", methods=["GET"])
def login():
    """Show login page."""
    # Attempt to retrieve access token from cookies
    access_token = request.cookies.get("access_token")
    try:
        if access_token:
            # Decode the access token to extract author_id
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256'])
            author_id = payload.get('sub', {}).get('user', {}).get('id')
            # Query author and their posts from the database
            author = prisma.user.find_unique(where={"id": author_id})
            posts = prisma.post.find_many(where={"authorId": author_id})

            # Truncate post content if it exceeds 40 characters
            for post in posts:
                if len(post.content) > 40:
                    post.content = post.content[:40] + "..."
            
            # Render the myblogs.html template with author information and posts
            return render_template("myblogs.html", showLogout=True, author=author, posts=posts)
        else:
            # If no access token is found, render the login.html template for signing in
            return render_template("login.html", signIn=True, showLogout=False)
    except jwt.ExpiredSignatureError:
        # Handle expired token error
        return render_template("login.html", signIn=True, showLogout=False, error="Token expired.")
    except jwt.InvalidTokenError:
        # Handle invalid token error
        return render_template("login.html", signIn=True, showLogout=False, error="Invalid token.")

@auth_routes.route("/login", methods=["POST"])
def login_post():
    """Login a user."""
    # Authenticate user with provided email and password
    user = authenticate(request.form["email"], request.form["password"])
    if user:
        # Clear session data
        session.clear()
        # Set success message and create access token for user
        session["success"] = f'Authenticated as {user.name} click to <a href="/logout">logout</a>.'
        token = create_access_token(identity={"user": {"id": user.id}})
        # Create response with redirect to user's posts and set access token cookie
        resp = make_response(redirect(url_for("user.user_posts", author_id=user.id, showLogout=True)))
        resp.set_cookie("access_token", token, httponly=True, max_age=86400)
        return resp
    # If authentication fails, set error message and redirect to login page
    session["error"] = "Authentication failed, please check your email and password."
    return redirect("/login")

@auth_routes.route("/logout", methods=["GET"])
def logout():
    """Logout a user."""
    # Clear session data and delete access token cookie
    session.clear()
    resp = make_response(redirect("/"))
    resp.delete_cookie("access_token")
    return resp

@auth_routes.route("/register", methods=["GET"])
def register():
    """Show register page."""
    # Render the register.html template
    return render_template("register.html", showLogout=False)

@auth_routes.route("/register", methods=["POST"])
def register_post():
    """Register a new user."""
    # Retrieve user input for registration
    email = request.form["email"]
    # Check if user with provided email already exists
    existing_user = prisma.user.find_unique(where={"email": email})
    if existing_user:
        # If user already exists, set error message and redirect to registration page
        session["error"] = "Registration failed, email already exists."
        return redirect("/register")
    # If user does not exist, register new user and set success message
    register_user(request.form["name"], email, request.form["password"])
    session["success"] = "Registration Successful, please login."
    return redirect("/login")
