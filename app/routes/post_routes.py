"""Post routes"""
from flask import Blueprint, request, redirect, abort,render_template
from app.utils.auth import authorize
from app.config import Config

prisma = Config.PRISMA

post_routes = Blueprint("post", __name__)



@post_routes.route("/post", methods=["POST"])
def create_post():
    """Create a new post"""
    title = request.form.get("title")
    content = request.form.get("content")

    if not title or not content:
        print("Missing required fields")
        abort(400)
    elif title and content:
        print("Creating post")
        prisma.post.create(
            data={
                "title": title,
                "content": content,

            }
        )
        return redirect(f"/")
    else:
        print("Unauthorized")
        abort(403)


@post_routes.route("/post", methods=["GET"])
def create_post_now():
    return render_template("write.html")

@post_routes.route("/submit_post", methods=["POST"])
def submit():
    return redirect("/")
