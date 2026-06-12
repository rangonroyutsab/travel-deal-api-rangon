from http import HTTPStatus

from flask import jsonify

from database.db import db
from database.models import Deal
from utils.validators import validate_input_data


class DealService:
    @staticmethod
    def create_deal(data):
        """
        Creates a new deal and stores it into the database
        """

        errors = validate_input_data(data)

        if errors:
            return jsonify(
                {"success": False, "message": "Validation failed", "errors": errors}
            ), HTTPStatus.BAD_REQUEST

        deal = Deal(
            destination=data["destination"],
            price=data["price"],
            platform=data["platform"],
            rating=data["rating"],
            travel_type=data["travel_type"],
        )

        db.session.add(deal)
        db.session.commit()

        return jsonify(
            {
                "success": True,
                "message": "Deal created successfully",
                "data": deal.to_dict(),
            }
        ), HTTPStatus.CREATED

    @staticmethod
    def get_all():
        """
        fetch all deals
        """

        deals = Deal.query.all()

        return jsonify(
            {
                "success": True,
                "message": "Deals fetched successfully",
                "data": [deal.to_dict() for deal in deals],
            }
        ), HTTPStatus.OK

    @staticmethod
    def get_by_id(id):
        """
        fetch deal with a specific id
        """

        deal = Deal.query.get(id)

        if not deal:
            return jsonify(
                {
                    "success": False,
                    "Message": "Deal not found",
                }
            ), HTTPStatus.NOT_FOUND

        return jsonify(
            {
                "success": True,
                "message": "Deal fetched successfully",
                "data": deal.to_dict(),
            }
        ), HTTPStatus.OK
