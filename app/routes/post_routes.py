"""Post routes"""
from flask import Blueprint, request, redirect, abort,render_template,url_for
from app.utils.auth import authorize
from app.config import Config
from flask import jsonify
from flask_jwt_extended import JWTManager
import jwt
from os import environ

SECRET_KEY = environ.get("SECRET_KEY", "secret-key")

prisma = Config.PRISMA

post_routes = Blueprint("post", __name__)

def get_author_id_from_token():
    access_token = request.cookies.get("access_token")
    if access_token:
        try:
            # Decode the access token to extract author_id
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256'])
            return payload.get('sub', {}).get('user', {}).get('id')
        except jwt.ExpiredSignatureError:
            # Handle expired token error
            return None
        except jwt.InvalidTokenError:
            # Handle invalid token error
            return None
    return None


@post_routes.route("/post", methods=["POST"])
def create_post():
    """Create a new post"""
    title = request.form.get("title")
    content = request.form.get("content")
    author_email = request.form.get("authorEmail")
    author_id = request.form.get("authorId")
    if not title or not content or not author_email or not author_id:
        print("Missing required fields")
        abort(400)
    elif authorize(author_id, request.cookies.get("access_token")):
        print("Creating post")
        prisma.post.create(
            data={
                "title": title,
                "content": content,
                "author": {"connect": {"email": author_email}},
            }
        )
        return redirect(f"/user/{author_id}/posts")
    else:
        print("Unauthorized")
        abort(403)


@post_routes.route("/post/<int:author_id>", methods=["GET"])
def create_post_now(author_id):

    if authorize(author_id, request.cookies.get("access_token")):
        author = prisma.user.find_unique(where={"id": author_id})
        if author:
            posts = prisma.post.find_many(where={"authorId": author_id})
            return render_template(
                "write.html", showLogout=True, author=author, posts=posts
            )
        return "User not found", 404
    abort(403)

@post_routes.route("/blogs", methods=["GET"])
def view_submitted():
    author = prisma.user.find_many()
    author_id = get_author_id_from_token()

    if  request.cookies.get("access_token"):
            author = prisma.user.find_unique(where={"id": author_id})
            posts = prisma.post.find_many()
            print(posts)
            return render_template(
                "posts.html", showLogout=True, author=author, posts=posts,)
    else:
        return render_template(
            "register.html", signIn = True
        )

@post_routes.route("/blogs", methods=["GET"])
def submit():
    return redirect(url_for(".view_submitted"), author_id = None)

@post_routes.route("/explore", methods=["GET"])
def explore():
    return render_template("get_started.html")
