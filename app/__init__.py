"""Entry point to the Flask application"""
from flask import Flask, redirect, render_template
from flask_jwt_extended import JWTManager
from .config import Config
from .routes.auth_routes import auth_routes
from .routes.user_routes import user_routes
from .routes.post_routes import post_routes
from flask_ckeditor import CKEditor
from .middlewares import setup_middlewares
import os
from datetime import timedelta

ckeditor = CKEditor()

def create_app(config_class=Config):
    """Create the Flask app instance"""
    app = Flask(__name__)
    ckeditor.init_app(app)
    UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    JWTManager(app)
    setup_middlewares(app)

    # Defining routes
    @app.route("/", methods=["GET"])
    def index():
        return render_template("landing.html", signIn = True)


    # @app.route("/write", methods=["GET"])
    # def landing():
    #     return render_template("write.html")

    # Registering blueprints from your routes modules
    app.register_blueprint(auth_routes)
    app.register_blueprint(user_routes, url_prefix="/user")
    app.register_blueprint(post_routes, url_prefix="/")


    return app

application = create_app()

application.run(host="0.0.0.0", debug=True)
