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
import math

prisma = Config.PRISMA

SECRET_KEY = environ.get("SECRET_KEY", "secret-key")


auth_routes = Blueprint("auth", __name__)


@auth_routes.route("/login", methods=["GET"])
def login():
    """Show login page."""
    access_token = request.cookies.get("access_token")
    try:
        page_number = request.args.get('page', default=1, type=int)
        posts_per_page = 9
        postsLength = prisma.post.count()
        posts = prisma.post.find_many(order={"createdAt": "desc"})[posts_per_page*(page_number-1):posts_per_page*(page_number)]
        navigation_range = math.ceil(postsLength / posts_per_page)
        print(navigation_range)
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
            return render_template("myblogs.html", posts=posts, author=author, navigation_range=navigation_range, postsLength=postsLength, showLogout=True)
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
    # """Handle user login post request.

    # This function handles the POST request for user login. It authenticates the user
    # by verifying the provided email and password. If authentication is successful,
    # it clears the session, sets a success message, generates an access token,
    # and redirects the user to the user_posts route. Otherwise, it sets an error message
    # and redirects the user to the login page.

    # Returns:
    #     Response: Redirects to appropriate route based on authentication status.
    # """
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
    # """Handle user logout request.

    # This function handles the GET request for user logout. It clears the session,
    # deletes the access token cookie, and redirects the user to the homepage.

    # Returns:
    #     Response: Redirects to the homepage.
    # """
    session.clear()
    resp = make_response(redirect("/"))
    resp.delete_cookie("access_token")
    return resp


@auth_routes.route("/register", methods=["GET"])
def register():
    """Show register page.

    This function renders the register page template.

    Returns:
        str: Rendered register page template.
    """
    return render_template("register.html", showLogout=False)


@auth_routes.route("/register", methods=["POST"])
def register_post():
    # """Handle user registration post request. This function handles the POST request for user registration. It validates
    # the provided email, checks if the user already exists, registers the user if not, and sets an appropriate message before redirecting to the login page.

    # Returns:
    #     Response: Redirects to appropriate route based on registration status.
    # """
    email = request.form["email"]
    existing_user = prisma.user.find_unique(where={"email": email})

    if existing_user:
        session["error"] = "Registration failed, email already exists."
        return redirect("/register")
    register_user(request.form["name"], email, request.form["password"])
    session["error"] = "Registration Successful, please login."
    return redirect("/login")


