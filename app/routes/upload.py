
def login():
    """Show login page."""
    access_token = request.cookies.get("access_token")
    try:
        if access_token:
            # Decode the access token to extract author_id
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256'])
            author_id = payload.get('sub', {}).get('user', {}).get('id')
            author = prisma.user.find_unique(where={"id": author_id})
            posts = prisma.post.find_many(where={"authorId": author_id})
            return render_template(
                    "posts.html", showLogout=True, author=author, posts=posts
                )
        else:
             return render_template(
                    "login.html", showLogout=True,
                )

    except jwt.ExpiredSignatureError:
        # Handle expired token error
        return render_template("login.html", signIn=True, showLogout=False, error="Token expired.")
    except jwt.InvalidTokenError:
        # Handle invalid token error
        return render_template("login.html", signIn=True, showLogout=False, error="Invalid token.")