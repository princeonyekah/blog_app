"""Routes for user pages"""
from flask import Blueprint, request, render_template, abort
from app.utils.auth import authorize
from app.config import Config

prisma = Config.PRISMA

user_routes = Blueprint("user", __name__)


@user_routes.route("/<int:id>/posts")
def user_posts(id):
    """Show all posts from a user"""
    if authorize(id, request.cookies.get("access_token")):
        author = prisma.user.find_unique(where={"id": id})
        if author:
            posts = prisma.post.find_many(where={"authorId": id})
            return render_template(
                "write.html", showLogout=True, author=author, posts=posts
            )
        return "User not found", 404
    abort(403)
