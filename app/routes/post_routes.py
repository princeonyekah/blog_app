"""Post routes"""
from flask import Blueprint, request, redirect, abort,render_template,url_for,Flask
from app.utils.auth import authorize
from app.config import Config
from flask import jsonify
from flask_jwt_extended import JWTManager
import jwt
from os import environ
from werkzeug.utils import secure_filename
import os
from flask import current_app as app

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

     # Handle file upload
    try:
        if not title or not content or not author_email or not author_id :
            print("Missing required fields")
            abort(400)
        elif authorize(author_id, request.cookies.get("access_token")):
            print("Creating post")
            image_file = request.files['image']
            image_filename = secure_filename(image_file.filename)
            new_post = prisma.post.create(
                data={
                    "title": title,
                    "content": content,
                    "author": {"connect": {"email": author_email}},
                    "imageFilename": image_filename
                }
            )
            print(new_post)
            # Save the file to a directory or database
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

            return redirect(f"/user/{author_id}/posts")
        else:
            print("Unauthorized")
            abort(403)
    except Exception as e:
        return render_template("login.html", signIn = True, error = str(e))



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
    try:
        author_id = get_author_id_from_token()

        if request.cookies.get("access_token"):
            author = prisma.user.find_unique(where={"id": author_id})
            posts = prisma.post.find_many()
            return render_template("all_post.html", showLogout=True, author=author, posts=posts)
        else:
            return render_template("register.html", signIn=True)
    except:
        return "User not found", 404

@post_routes.route("/explore", methods=["GET"])
def explore():
    return render_template("get_started.html")

# Shows alll the post on all_blogs.html
@post_routes.route("/all_blogs", methods=["GET"])
def all_blogs():
    posts = prisma.post.find_many()
    print(posts)
    return render_template("all_blogs.html", posts=posts)

# ---Edit Post---

@post_routes.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    # """Edit an existing post"""
    # author_id = get_author_id_from_token()
    # if not author_id:
    #     abort(403)  # User is not authorized

    # post = prisma.post.find_unique(where={"id": post_id})
    # if not post:
    #     abort(404)  # Post not found

    # if post.authorId != author_id:
    #     abort(403)  # User is not the author of the post

    # if request.method == "POST":
    #     title = request.form.get("title")
    #     content = request.form.get("content")
    #     # Update the post in the database
    #     prisma.post.update(
    #         where={"id": post_id},
    #         data={"title": title, "content": content}
    #     )
    #     return redirect(url_for("post.create_post_now", author_id=post.authorId)
    # Check if the user is authorized to edit posts
    author_id = get_author_id_from_token()
    author = prisma.user.find_unique(where={"id": author_id})
    if not author_id:
        abort(403)  # User is not authorized

    # Fetch the existing post from the database
    post = prisma.post.find_unique(where={"id": post_id})
    print(post)
    if not post:
        abort(404)  # Post not found

    # Check if the current user is the author of the post
    if post.authorId != author_id:
        abort(403)  # User is not the author of the post

    if request.method == "POST":
        # Process the form submission to update the post
        title = request.form.get("title")
        content = request.form.get("content")
        # Update the post in the database
        prisma.post.update(
            where={"id": post_id},
            data={"title": title, "content": content}
        )
        # Redirect to the page displaying all posts by the author
        return redirect(url_for("post.create_post_now", author_id=post.authorId))

    # Render the edit form with pre-filled data
    return render_template("edit_post.html", post=post, author=author, showLogout=True)
