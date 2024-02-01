"""Entry point to the Flask application"""
from flask import Flask, redirect, render_template
from flask_jwt_extended import JWTManager
from .config import Config
from .routes.auth_routes import auth_routes
from .routes.user_routes import user_routes
from .routes.post_routes import post_routes
from .middlewares import setup_middlewares
from prisma_client import PrismaClient


def create_app(config_class=Config):
    """Create the Flask app instance"""
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = config_class.SECRET_KEY
    app.config.from_object(config_class)
    JWTManager(app)
    setup_middlewares(app)

    prisma = PrismaClient()

    #Using the PrismaClient instance to connect to the database
    @app.before_request
    def before_request():
        prisma.connect()

    @app.teardown_request
    def teardown_request():
        prisma.disconnect()


    # Defining routes
    @app.route("/", methods=["GET"])
    def index():
        #Get the blog data from the database
        #Pass the data to the template
        #Render the template
        blogs = prisma.blogs.find_many()
        return render_template("landing.html", blogs=blogs, signIn = True)


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
