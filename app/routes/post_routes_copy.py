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

    if not title or not content :
        print("Missing required fields")
        abort(400)
    else:
        print("Creating post")
        prisma.blogpost.create(
            data={
                "title": title,
                "content": content,

            }
        )
        return redirect("/")







