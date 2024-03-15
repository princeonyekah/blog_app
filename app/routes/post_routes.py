"""Post routes"""
import math
from flask import Blueprint, request, redirect, abort,render_template,url_for,Flask
from app.utils.auth import authorize
from flask_ckeditor import CKEditor
from app.config import Config
from flask import jsonify
from flask_jwt_extended import JWTManager
import jwt
from os import environ
from werkzeug.utils import secure_filename
import os
from flask import current_app as app

from markupsafe import Markup
from flask import flash



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


#displays all the blogs on the website
@post_routes.route("/all_blogs/<sectionvalue>", methods=["GET"])
def all_blogs(sectionvalue):
    page_number = int(sectionvalue[3:])
    postsLength = prisma.post.count()
    posts_per_page = 9
    posts = prisma.post.find_many(order={"createdAt": "desc"})[posts_per_page*(page_number-1):posts_per_page*(page_number)]
    author_id = get_author_id_from_token()
    navigation_range = math.ceil(postsLength / posts_per_page)

    if get_author_id_from_token():
        try:
            author_id = get_author_id_from_token()
            author = prisma.user.find_unique(where={"id": author_id})
            # Truncate post content if it's longer than 40 characters
            for post in posts:
                post.content = Markup(post.content)
                # Example custom markup
                if len(post.content) > 40:
                    post.content = post.content[:40] + "..."
            return render_template("all_blogs.html", posts=posts, navigation_range=navigation_range, postsLength=postsLength, author=author, showLogout=True)
        except Exception as e:
            return render_template("all_blogs.html", posts=posts, navigation_range=navigation_range, postsLength=postsLength, error=str(e))
    else:
        for post in posts:
            post.content = Markup(post.content)
            if len(post.content) > 40:
                post.content = post.content[:40] + "..."
        return render_template("all_blogs.html", posts=posts, navigation_range=navigation_range, postsLength=postsLength, author= None)

#displays blogs owned by writer
@post_routes.route("/blogs", methods=["GET"])
def view_submitted():
    author = prisma.user.find_many()
    author_id = get_author_id_from_token()

    page_number = request.args.get('page', default=1, type=int)
    posts_per_page = 9
    postsLength = prisma.post.count()
    posts = prisma.post.find_many(order={"createdAt": "desc"})[posts_per_page*(page_number-1):posts_per_page*(page_number)]
    author_id = get_author_id_from_token()
    navigation_range = math.ceil(postsLength / posts_per_page)
    print(navigation_range)

    if request.cookies.get("access_token"):
        try:
            author_id = get_author_id_from_token()
            author = prisma.user.find_unique(where={"id": author_id})
            posts = prisma.post.find_many(where={"authorId": author_id},
                                            order={"createdAt": "desc"})
            # Truncate post content if it's longer than 40 characters
            for post in posts:
                post.content = Markup(post.content)
                if len(post.content) > 40:
                    post.content = post.content[:40] + "..."
            return render_template("myblogs.html", posts=posts, navigation_range=navigation_range, postsLength=postsLength, author=author, showLogout=True)
        except Exception as e:
            return render_template("login.html",signIn= True, error=str(e))
    else:
        return render_template("login.html",signIn= True)

@post_routes.route("/blog/<int:post_id>", methods=["GET"])
def view_post(post_id):
    post = prisma.post.find_unique(where={"id": post_id}, include={"author": True})
    author_id = get_author_id_from_token()
    author = 0
    if author_id:
        author = prisma.user.find_unique(where={"id": author_id})
        post.content = Markup(post.content)
        return render_template("read_more.html", post=post, showLogout=True, author= author )
    if post:
        post.content = Markup(post.content)
        return render_template("read_more.html", post=post, author= author )
    abort(404)

#Creates posts
@post_routes.route("/post/<int:author_id>", methods=["GET"])
def create_post_now(author_id):

    if authorize(author_id, request.cookies.get("access_token")):
        author = prisma.user.find_unique(where={"id": author_id})
        if author:
            posts = prisma.post.find_many(where={"authorId": author_id})
            return render_template(
                "write.html", showLogout=True, author=author, posts=posts
            )
        return render_template("login.html", signIn = True)
    else:
        return render_template("login.html", signIn = True)

@post_routes.route("/post", methods=["POST"])
def create_post():
    """Create a new post"""
    title = request.form.get("title")

    content = Markup(request.form.get('ckeditor'))
    author_email = request.form.get("authorEmail")
    author_id = request.form.get("authorId")

    try:
        if not title or not content or not author_email or not author_id:
            print("Missing required fields")
            abort(400)
        elif authorize(author_id, request.cookies.get("access_token")):
            existing_post = prisma.post.find_first(where={"title": title, "content": content})
            if existing_post:
                print("Post already exists")
                # Handle the case where the post already exists (e.g., show an error message)
                return render_template("error.html", error="Post already exists")
            else:
                print("Creating post")
                image_file = request.files['image']
                image_filename = secure_filename(image_file.filename)
                new_post = prisma.post.create(
                    data={
                        "title": title,
                        "content": content,
                        "author": {"connect": {"email": author_email}},
                        "imageFilename": image_filename  # Optionally, save image filename
                    }
                )
                # Save the file to a directory or database
                image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

                return redirect(f"/user/{author_id}/posts")
        else:
            print("Unauthorized")
            return render_template("login.html", signIn=True, error="Unauthorized")
    except Exception as e:
        return render_template("login.html", signIn=True, error=str(e))



# Redirects on request for myblogs
@post_routes.route("/myblogs", methods=["GET"])
def myblogs():
    return redirect(url_for('post.view_submitted'))


# ---Edit Post---
@post_routes.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    author_id = get_author_id_from_token()
    if not author_id:
        abort(403)  # User is not authorized

    author = prisma.user.find_unique(where={"id": author_id})
    if not author:
        abort(404)  # Author not found

    post = prisma.post.find_unique(where={"id": post_id})
    user = prisma.user.find_unique(where={"id": author_id})
    if not post:
        abort(404)  # Post not found

    if post.authorId != author_id:
        abort(403)  # User is not the author of the post

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        image_file = request.files['image']
        image_filename = secure_filename(image_file.filename)

        prisma.post.update(
            where={"id": post_id},
            data={"title": title,
                  "content": content,
                  "imageFilename": image_filename}
        )
        flash("Post updated successfully", "success")
        return redirect(url_for("post.view_post", post_id=post_id))

    return render_template("edit_post.html", post=post, author=author,user = user, showLogout=True)


@post_routes.route("/blog/<int:post_id>", methods=["GET"])
def view_post(post_id):
    post = prisma.post.find_unique(where={"id": post_id}, include={"author": True})
    author_id = get_author_id_from_token()

    #Check if author_id is None
    if author_id is None:
        # If author_id is None, then the user is not logged in, take them to the login page

        # it should tell the user that they need to login to view the post
        message = "You need to login to view this post"
        return render_template("login.html", signIn=True, message=message)

    author = 0
    if author_id:
        author = prisma.user.find_unique(where={"id": author_id})
        return render_template("read_more.html", post=post, showLogout=True, author= author )

    abort(404)


# Goes to the user_profile page if user is authorized
@post_routes.route("/user_profile/<int:author_id>", methods=["GET"])
def user_profile(author_id):
    if authorize(author_id, request.cookies.get("access_token")):
        author = prisma.user.find_unique(where={"id": author_id})
        if author:
            return render_template("user_profile.html", showLogout=True, author=author)
        return "User not found", 404
    abort(403)

# Edit user_profile
@post_routes.route("/edit_user_profile/<int:author_id>", methods=["GET", "POST"])
def edit_user_profile(author_id):
    if authorize(author_id, request.cookies.get("access_token")):
        author = prisma.user.find_unique(where={"id": author_id})
        print(author)
        if not author:
            return "User not found", 404

        if request.method == "GET":
            # Render the edit form with pre-filled data
            return render_template("edit_user_profile.html", author=author, showLogout=True)

        if request.method == "POST":
            # Process the form submission to update the user profile
            UPLOAD_FOLDER = 'app/static/uploads'
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            email = request.form.get("email")
            profilePic = request.files['profilePic']
            profilePic.filename = secure_filename(profilePic.filename)
            print(profilePic.filename)

            # Check if the user has uploaded a profile picture
            if profilePic.filename == '':
                default_image_path = 'app/static/uploads/default-avatar-icon.jpg'
                if not os.path.exists(default_image_path):
                    return "Default image not found", 500

                # Secures the filename
                filename = secure_filename(os.path.basename(default_image_path))
                default_image_destination = os.path.join(UPLOAD_FOLDER, filename)

                # Copy the default image to the upload folder if it doesn't exist there
                if not os.path.exists(default_image_destination):
                    shutil.copy(default_image_path, default_image_destination)

                profilePic.filename = filename

            # Create the upload folder if it doesn't exist
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            profilePic.save(os.path.join(UPLOAD_FOLDER, profilePic.filename))


            # Update the user profile in the database
            prisma.user.update(
                where={"id": author_id},
                data={"firstName": first_name,
                      "lastName": last_name,
                      "email": email,
                      "profilePic": profilePic.filename}
            )
            # Redirect to the user profile page
            return redirect(url_for("post.user_profile", author_id=author_id))
        # Render the edit form with pre-filled data
        return render_template("edit_user_profile.html", author=author, showLogout=True)
    abort(403)

@post_routes.route("/update_profile/<int:author_id>", methods=["GET", "POST"])
def update_profile(author_id):
    if request.method == "GET":
        try:
            # Retrieve the author information for displaying the edit form
            author = prisma.user.find_unique(where={"id": author_id})

            if not author:
                return "User not found", 404
        except Exception as e:
            # Render the edit_user_profile.html template with author information
            return render_template("edit_user_profile.html", author=author, showLogout=True, error=str(e))

    if request.method == "POST":
        # Retrieve form data from the request
        data = request.form
        UPLOAD_FOLDER = 'app/static/uploads'

        # Retrieve the author information for updating
        author = prisma.user.find_unique(where={"id": author_id})
        if not author:
            return "User not found", 404

        # Extract new user data from the form
        new_username = data.get("username")
        new_email = data.get("email")
        new_bio = data.get("bio")

        if not all([new_username, new_email, new_bio]):
            return "Missing form data", 400

        # Retrieve the profile picture file from the request
        new_profilePic = request.files.get('profilePic')
        if new_profilePic:
            # Save the profile picture file to the upload folder
            filename = secure_filename(new_profilePic.filename)
            new_profilePic.save(os.path.join(UPLOAD_FOLDER, filename))
        else:
            return "No file uploaded", 400

        try:
            # Update user information in the database
            prisma.user.update(where={"id": author_id},
                                data={"name": new_username,
                                      "email": new_email,
                                      "bio": new_bio,
                                      "profilePic": filename
                                      })
        except Exception as e:
            # Rollback the file saving if database update fails
            os.remove(os.path.join(UPLOAD_FOLDER, filename))
            return str(e), 400

        return redirect(url_for("post.user_profile", author_id=author_id))

    # If the request method is neither GET nor POST, render the edit form with author information
    return render_template("edit_user_profile.html", author=author, showLogout=True)


@post_routes.route("/delete/<int:post_id>", methods=["GET", "POST"])
def delete_post(post_id):
    author_id = get_author_id_from_token()
    if not author_id:
        abort(403)
    post = prisma.post.find_unique(where={"id": post_id})
    if not post:
        abort(404)
    if post.authorId != author_id:
        abort(403)
    prisma.post.delete(where={"id": post_id})
    return redirect(f"/user/{author_id}/posts")

# Confirmatiion of Delete
@post_routes.route("/confirm_delete/<int:post_id>", methods=["GET"])
def confirm_delete(post_id):
    author_id = get_author_id_from_token()
    if not author_id:
        abort(403)
    post = prisma.post.find_unique(where={"id": post_id})
    if not post:
        abort(404)
    if post.authorId != author_id:
        abort(403)
    return render_template("confirm_delete.html", post=post, showLogout=True)

# Learn
@post_routes.route("/learn", methods = ["GET"])
def learn():
    if request.cookies.get("access_token"):
        author_id = get_author_id_from_token()
        author = prisma.user.find_unique(where={"id": author_id})
        return render_template("learn.html", showLogout=True, author=author)
    return render_template('learn.html')

# Explore
@post_routes.route("/explore", methods=["GET"])
def explore():
    if request.cookies.get("access_token"):
        author_id = get_author_id_from_token()
        author = prisma.user.find_unique(where={"id": author_id})
        return render_template("explore.html", showLogout=True, author=author)
    return render_template("explore.html")

def perform_search(query):
    # Implement the actual search logic here
    search_results = []  # Define the variable and assign an initial value
    query = request.args.get('query')
    # Code for performing the search and populating search_results
    # ...
    return search_results, query

@post_routes.route("/search", methods=["GET"])
def search_posts():
    query = request.args.get('query')

    # Search in the User table by name and include their posts
    user_results = prisma.user.find_many(where={"name": {"contains": query}}, include={"posts": True})

    # Extract the posts from the user results
    post_results = [post for user in user_results for post in user.posts]

    # It is not supposed to log the user in if the user is not logged in
    if request.cookies.get("access_token"):
        author_id = get_author_id_from_token()
        author = prisma.user.find_unique(where={"id": author_id})
        return render_template("search_results.html", posts=post_results, author=author, showLogout=True)

    return render_template("search_results.html", posts=post_results)

@post_routes.route("/filter", methods=["GET"])
def filter_posts():
    category = request.args.get('category')

    filtered_posts = perform_filter(category)
    # Render a template with the filtered posts
    return render_template("filtered_posts.html", posts=filtered_posts)

def perform_filter(category):
    # Implement the actual filter logic here
    filtered_posts = []  # Define the variable and assign an initial value
    category = request.args.get('category')
    # Code for performing the filter and populating filtered_posts
    # ...
    return filtered_posts, category

@post_routes.route("/sort", methods=["GET"])
def sort_posts():
    # Now you can use 'sort_by' to sort posts by date or popularity
    # You need to implement the actual sort logic
    sorted_posts = []  # Define the variable and assign an initial value
    # Code for sorting the posts and populating sorted_posts
    # ...
    return render_template("sorted_posts.html", posts=sorted_posts)