import logging
from http import HTTPStatus

from flask import Flask
from flask import jsonify
from config import Config

from database.db import db
from routes.deal_routes import deal_bp
from utils.stats import ApiStats


def create_app():
    """
    Application Factory
    """

    # Initialize the app
    app = Flask(__name__)

    # Load Config
    app.config.from_object(Config)

    # Logging
    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s - "
            "%(levelname)s - "
            "%(message)s"
        ),
    )

    # Initialize the Database
    db.init_app(app)

    # Register the blueprint
    app.register_blueprint(deal_bp, url_prefix="/deals")

    @app.after_request
    def track_request_stats(response):
        """
        Track API request statistics after each completed request.
        """

        ApiStats.record_request(response.status_code)

        return response

    # Create Tables
    with app.app_context():
        db.create_all()

    @app.route("/")
    def health():
        """
        check if the server is running
        """

        logging.info("Health check request successful")

        return {"message": "Travel Deals API in running!"}

    @app.route("/stats", methods=["GET"])
    def get_stats():
        """
        Fetch in-memory API usage statistics.
        """

        logging.info("API stats request received")

        return jsonify(
            {
                "success": True,
                "message": "API stats fetched successfully",
                "data": ApiStats.get_stats(),
            }
        ), HTTPStatus.OK

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
