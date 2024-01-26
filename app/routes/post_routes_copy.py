"""Post routes"""
from flask import Blueprint, request, redirect, abort
from app.utils.auth import authorize
from app.config import Config

prisma = Config.PRISMA

submitpost_routes = Blueprint("submitpost", __name__)


@submitpost_routes.route("/", methods=["POST"])
def create_post():
    """Create a new post"""
    title = request.form.get("title")
    content = request.form.get("content")
    author_email = request.form.get("authorEmail")
    author_id = request.form.get("authorId")
    print("author_id: ", author_id)
    if not title or not content or not author_email or not author_id:
        print("Missing required fields")
        abort(400)
   
    elif authorize(author_id, request.cookies.get("access_token")):
        print("Creating post")
        prisma.blogpost.create(
            data={
                "title": title,
                "content": content,
                "author": {"connect": {"email": author_email}},
            }
        )
        return redirect(f"/")
    else:
        print("Unauthorized")
        abort(403)



