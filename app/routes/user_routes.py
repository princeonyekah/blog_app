"""Routes for user pages"""
from flask import Blueprint, request, render_template, abort
from app.utils.auth import authorize
from app.config import Config

prisma = Config.PRISMA

user_routes = Blueprint("user", __name__)


@user_routes.route("/<int:author_id>/posts")
def user_posts(author_id):
    """Show all posts from a user"""
    if authorize(author_id, request.cookies.get("access_token")):
        author = prisma.user.find_unique(where={"id": author_id})
        if author:
            posts = prisma.post.find_many(where={"authorId": author_id})
            return render_template(
                "posts.html", showLogout=True, author=author, posts=posts
            )
        return "User not found", 404
    abort(403)
