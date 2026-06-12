from flask import Flask
from config import Config

from database.db import db
from routes.deal_routes import deal_bp


def create_app():
    """
    Application Factory
    """

    # Initialize the app
    app = Flask(__name__)

    # Load Config
    app.config.from_object(Config)

    # Initialize the Database
    db.init_app(app)

    # Register the blueprint
    app.register_blueprint(deal_bp, url_prefix="/deals")

    # Create Tables
    with app.app_context():
        db.create_all()

    @app.route("/")
    def health():
        """
        check if the server is running
        """

        return {"message": "Travel Deals API in running!"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
