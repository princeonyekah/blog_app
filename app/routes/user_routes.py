"""Routes for user pages"""
from flask import Blueprint, request, render_template, abort
from app.utils.auth import authorize
from app.config import Config
from markupsafe import Markup
import math

prisma = Config.PRISMA

user_routes = Blueprint("user", __name__)


@user_routes.route("/<int:author_id>/posts")
def user_posts(author_id):
    """Show all posts from a user"""

    page_number = request.args.get('page', default=1, type=int)
    posts_per_page = 9
    postsLength = prisma.post.count()
    posts = prisma.post.find_many(order={"createdAt": "desc"})[posts_per_page*(page_number-1):posts_per_page*(page_number)]
    navigation_range = math.ceil(postsLength / posts_per_page)
    print(navigation_range)

    if authorize(author_id, request.cookies.get("access_token")):
        author = prisma.user.find_unique(where={"id": author_id})
        if author:
            posts = prisma.post.find_many(where={"authorId": author_id},
                                           order = {"createdAt": "desc"})
            for post in posts:
                post.content = Markup(post.content)
                if len(post.content) > 40:
                    post.content = post.content[:40] + "..."
            return render_template(
                "myblogs.html", showLogout=True, author=author, posts=posts,navigation_range=navigation_range, postsLength=postsLength
            )
        return "User not found", 404
    abort(403)

# Goes to the user_profile page if user is authorized
@user_routes.route("/<int:author_id>/user_profile")
def user_profile(author_id):
    if authorize(author_id, request.cookies.get("access_token")):
        author = prisma.user.find_unique(where={"id": author_id})
        if author:
            return render_template("user_profile.html", showLogout=True, author=author)
        return "User not found", 404
    abort(403)

# For editing the user profile
@user_routes.route("/<int:author_id>/edit_profile", methods=["GET", "POST"])
def edit_profile(author_id):
    if authorize(author_id, request.cookies.get("access_token")):
        author = prisma.user.find_unique(where={"id": author_id})
        if author:
            if request.method == "POST":
                data = request.form
                prisma.user.update(where={"id": author_id}, data=data)
                return render_template("user_profile.html", showLogout=True, author=author)
            return render_template("edit_profile.html", showLogout=True, author=author)
        return "User not found", 404
    abort(403)