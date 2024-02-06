"""Entry point to the Flask application"""
from flask import Flask, redirect, render_template
from flask_jwt_extended import JWTManager
from .config import Config
from .routes.auth_routes import auth_routes
from .routes.user_routes import user_routes
from .routes.post_routes import post_routes
from .middlewares import setup_middlewares
import os



def create_app(config_class=Config):
    """Create the Flask app instance"""
    app = Flask(__name__)
    UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

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
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

