import logging
from http import HTTPStatus

from flask import jsonify
from sqlalchemy import select

from database.db import db
from database.models import Deal
from utils.stats import ApiStats
from utils.validators import (
    is_empty,
    validate_filter_query,
    validate_input_data,
    validate_search_query,
    validate_sort_query,
)


class DealService:
    recently_viewed_deals = []

    @staticmethod
    def _deal_list_response(message, deals):
        """
        Build a response for a list of deals.
        """

        return jsonify(
            {
                "success": True,
                "message": message,
                "data": [deal.to_dict() for deal in deals],
            }
        ), HTTPStatus.OK

    @staticmethod
    def _execute_deal_statement(statement):
        """
        Execute a deal select statement.
        """

        return db.session.execute(statement).scalars().all()

    @staticmethod
    def _apply_search_filters(statement, data):
        """
        Apply search filters to a deal statement.
        """

        destination = data.get("destination")
        platform = data.get("platform")
        travel_type = data.get("travel_type")

        if not is_empty(destination):
            statement = statement.where(
                Deal.destination.ilike(f"%{destination.strip()}%")
            )

        if not is_empty(platform):
            statement = statement.where(Deal.platform.ilike(f"%{platform.strip()}%"))

        if not is_empty(travel_type):
            statement = statement.where(
                Deal.travel_type.ilike(f"%{travel_type.strip()}%")
            )

        return statement

    @staticmethod
    def _apply_price_filters(statement, data):
        """
        Apply price filters to a deal statement.
        """

        min_price = data.get("min_price")
        max_price = data.get("max_price")

        if not is_empty(min_price):
            statement = statement.where(Deal.price >= float(min_price))

        if not is_empty(max_price):
            statement = statement.where(Deal.price <= float(max_price))

        return statement

    @staticmethod
    def _apply_sorting(statement, data):
        """
        Apply sorting to a deal statement.
        """

        sort_by = data.get("sort_by")
        order = data.get("order", "asc").lower()
        sort_column = getattr(Deal, sort_by)

        if order == "desc":
            return statement.order_by(sort_column.desc())

        return statement.order_by(sort_column.asc())

    @staticmethod
    def _build_deal_statement(
        data,
        apply_search=False,
        apply_price=False,
        apply_sort=False,
    ):
        """
        Build a deal statement by applying requested query conditions.
        """

        statement = select(Deal)

        if apply_search:
            statement = DealService._apply_search_filters(statement, data)

        if apply_price:
            statement = DealService._apply_price_filters(statement, data)

        if apply_sort:
            statement = DealService._apply_sorting(statement, data)

        return statement

    @staticmethod
    def _track_recent_deal(deal_id):
        """
        Track recently viewed deal ids.
        """

        if deal_id in DealService.recently_viewed_deals:
            DealService.recently_viewed_deals.remove(deal_id)

        DealService.recently_viewed_deals.insert(0, deal_id)
        DealService.recently_viewed_deals = DealService.recently_viewed_deals[:5]

    @staticmethod
    def _track_deal_view(deal_id):
        """
        Track a successful deal view.
        """

        DealService._track_recent_deal(deal_id)
        ApiStats.record_deal_view(deal_id)

    @staticmethod
    def _remove_tracked_deal(deal_id):
        """
        Remove deleted deals from in-memory tracking.
        """

        if deal_id in DealService.recently_viewed_deals:
            DealService.recently_viewed_deals.remove(deal_id)

        ApiStats.remove_deal(deal_id)

    @staticmethod
    def create_deal(data):
        """
        Creates a new deal and stores it into the database
        """

        errors = validate_input_data(data)

        if errors:
            logging.warning("Deal creation validation failed: %s", errors)
            return jsonify(
                {"success": False, "message": "Validation failed", "errors": errors}
            ), HTTPStatus.BAD_REQUEST

        try:
            deal = Deal(
                destination=data["destination"],
                price=data["price"],
                platform=data["platform"],
                rating=data["rating"],
                travel_type=data["travel_type"],
            )

            db.session.add(deal)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            logging.error("Failed to create deal: %s", error)
            return jsonify(
                {"success": False, "message": "Failed to create deal"}
            ), HTTPStatus.INTERNAL_SERVER_ERROR

        logging.info("Deal created successfully with id: %s", deal.id)

        return jsonify(
            {
                "success": True,
                "message": "Deal created successfully",
                "data": deal.to_dict(),
            }
        ), HTTPStatus.CREATED

    @staticmethod
    def update_deal(deal_id, data):
        """
        Update an existing deal.
        """

        errors = validate_input_data(data)

        if errors:
            logging.warning("Deal update validation failed: %s", errors)
            return jsonify(
                {"success": False, "message": "Validation failed", "errors": errors}
            ), HTTPStatus.BAD_REQUEST

        try:
            deal = db.session.get(Deal, deal_id)
        except Exception as error:
            logging.error("Failed to fetch deal with id %s: %s", deal_id, error)
            return jsonify(
                {"success": False, "message": "Failed to update deal"}
            ), HTTPStatus.INTERNAL_SERVER_ERROR

        if not deal:
            logging.warning("Deal not found with id: %s", deal_id)
            return jsonify(
                {"success": False, "message": "Deal not found"}
            ), HTTPStatus.NOT_FOUND

        try:
            deal.destination = data["destination"]
            deal.price = data["price"]
            deal.platform = data["platform"]
            deal.rating = data["rating"]
            deal.travel_type = data["travel_type"]

            db.session.commit()
        except Exception as error:
            db.session.rollback()
            logging.error("Failed to update deal with id %s: %s", deal_id, error)
            return jsonify(
                {"success": False, "message": "Failed to update deal"}
            ), HTTPStatus.INTERNAL_SERVER_ERROR

        logging.info("Deal updated successfully with id: %s", deal_id)

        return jsonify(
            {
                "success": True,
                "message": "Deal updated successfully",
                "data": deal.to_dict(),
            }
        ), HTTPStatus.OK

    @staticmethod
    def delete_deal(deal_id):
        """
        Delete an existing deal.
        """

        try:
            deal = db.session.get(Deal, deal_id)

            if not deal:
                logging.warning("Deal not found with id: %s", deal_id)
                return jsonify(
                    {"success": False, "message": "Deal not found"}
                ), HTTPStatus.NOT_FOUND

            db.session.delete(deal)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            logging.error("Failed to delete deal with id %s: %s", deal_id, error)
            return jsonify(
                {"success": False, "message": "Failed to delete deal"}
            ), HTTPStatus.INTERNAL_SERVER_ERROR

        DealService._remove_tracked_deal(deal_id)
        logging.info("Deal deleted successfully with id: %s", deal_id)

        return jsonify(
            {
                "success": True,
                "message": "Deal deleted successfully",
            }
        ), HTTPStatus.OK

    @staticmethod
    def get_all():
        """
        fetch all deals
        """

        try:
            statement = select(Deal)
            deals = DealService._execute_deal_statement(statement)
        except Exception as error:
            logging.error("Failed to fetch deals: %s", error)
            return jsonify(
                {"success": False, "message": "Failed to fetch deals"}
            ), HTTPStatus.INTERNAL_SERVER_ERROR

        logging.info("Deals fetched successfully. Total deals: %s", len(deals))

        return jsonify(
            {
                "success": True,
                "message": "Deals fetched successfully",
                "data": [deal.to_dict() for deal in deals],
            }
        ), HTTPStatus.OK

    @staticmethod
    def search_deals(data):
        """
        Search deals using query parameters.
        """

        errors = validate_search_query(data)

        if errors:
            logging.warning("Deal search validation failed: %s", errors)
            return jsonify(
                {"success": False, "message": "Validation failed", "errors": errors}
            ), HTTPStatus.BAD_REQUEST

        try:
            statement = DealService._build_deal_statement(data, apply_search=True)
            deals = DealService._execute_deal_statement(statement)
        except Exception as error:
            logging.error("Failed to search deals: %s", error)
            return jsonify(
                {"success": False, "message": "Failed to search deals"}
            ), HTTPStatus.INTERNAL_SERVER_ERROR

        logging.info("Deals searched successfully. Total deals: %s", len(deals))

        return DealService._deal_list_response(
            "Deals searched successfully",
            deals,
        )

    @staticmethod
    def filter_deals(data):
        """
        Filter deals by price range.
        """

        errors = validate_filter_query(data)

        if errors:
            logging.warning("Deal filter validation failed: %s", errors)
            return jsonify(
                {"success": False, "message": "Validation failed", "errors": errors}
            ), HTTPStatus.BAD_REQUEST

        try:
            statement = DealService._build_deal_statement(data, apply_price=True)
            deals = DealService._execute_deal_statement(statement)
        except Exception as error:
            logging.error("Failed to filter deals: %s", error)
            return jsonify(
                {"success": False, "message": "Failed to filter deals"}
            ), HTTPStatus.INTERNAL_SERVER_ERROR

        logging.info("Deals filtered successfully. Total deals: %s", len(deals))

        return DealService._deal_list_response(
            "Deals filtered successfully",
            deals,
        )

    @staticmethod
    def sort_deals(data):
        """
        Sort deals by a valid field and order.
        """

        errors = validate_sort_query(data)

        if errors:
            logging.warning("Deal sort validation failed: %s", errors)
            return jsonify(
                {"success": False, "message": "Validation failed", "errors": errors}
            ), HTTPStatus.BAD_REQUEST

        try:
            statement = DealService._build_deal_statement(data, apply_sort=True)
            deals = DealService._execute_deal_statement(statement)
        except Exception as error:
            logging.error("Failed to sort deals: %s", error)
            return jsonify(
                {"success": False, "message": "Failed to sort deals"}
            ), HTTPStatus.INTERNAL_SERVER_ERROR

        logging.info("Deals sorted successfully. Total deals: %s", len(deals))

        return DealService._deal_list_response(
            "Deals sorted successfully",
            deals,
        )

    @staticmethod
    def get_recent_deals():
        """
        Fetch recently viewed deals.
        """

        if not DealService.recently_viewed_deals:
            logging.info("No recently viewed deals found")
            return DealService._deal_list_response(
                "No recently viewed deals found",
                [],
            )

        try:
            statement = select(Deal).where(
                Deal.id.in_(DealService.recently_viewed_deals)
            )
            deals = DealService._execute_deal_statement(statement)
        except Exception as error:
            logging.error("Failed to fetch recently viewed deals: %s", error)
            return jsonify(
                {"success": False, "message": "Failed to fetch recently viewed deals"}
            ), HTTPStatus.INTERNAL_SERVER_ERROR

        deals_by_id = {deal.id: deal for deal in deals}
        sorted_deals = [
            deals_by_id[deal_id]
            for deal_id in DealService.recently_viewed_deals
            if deal_id in deals_by_id
        ]

        logging.info(
            "Recently viewed deals fetched successfully. Total deals: %s",
            len(sorted_deals),
        )

        return DealService._deal_list_response(
            "Recently viewed deals fetched successfully",
            sorted_deals,
        )

    @staticmethod
    def get_popular_deals():
        """
        Fetch viewed deals ordered by view count.
        """

        view_counts = ApiStats.get_deal_view_counts()

        if not view_counts:
            logging.info("No popular deals found")
            return jsonify(
                {
                    "success": True,
                    "message": "No popular deals found",
                    "data": [],
                }
            ), HTTPStatus.OK

        try:
            statement = select(Deal).where(Deal.id.in_(list(view_counts.keys())))
            deals = DealService._execute_deal_statement(statement)
        except Exception as error:
            logging.error("Failed to fetch popular deals: %s", error)
            return jsonify(
                {"success": False, "message": "Failed to fetch popular deals"}
            ), HTTPStatus.INTERNAL_SERVER_ERROR

        deals_by_id = {deal.id: deal for deal in deals}
        sorted_view_counts = sorted(
            view_counts.items(),
            key=lambda view_count: view_count[1],
            reverse=True,
        )
        popular_deals = []

        for deal_id, view_count in sorted_view_counts:
            deal = deals_by_id.get(deal_id)

            if not deal:
                ApiStats.remove_deal(deal_id)
                continue

            deal_data = deal.to_dict()
            deal_data["view_count"] = view_count
            popular_deals.append(deal_data)

        logging.info(
            "Popular deals fetched successfully. Total deals: %s",
            len(popular_deals),
        )

        return jsonify(
            {
                "success": True,
                "message": "Popular deals fetched successfully",
                "data": popular_deals,
            }
        ), HTTPStatus.OK

    @staticmethod
    def get_by_id(id):
        """
        fetch deal with a specific id
        """

        try:
            deal = db.session.get(Deal, id)
        except Exception as error:
            logging.error("Failed to fetch deal with id %s: %s", id, error)
            return jsonify(
                {"success": False, "message": "Failed to fetch deal"}
            ), HTTPStatus.INTERNAL_SERVER_ERROR

        if not deal:
            logging.warning("Deal not found with id: %s", id)
            return jsonify(
                {
                    "success": False,
                    "Message": "Deal not found",
                }
            ), HTTPStatus.NOT_FOUND

        logging.info("Deal fetched successfully with id: %s", id)
        DealService._track_deal_view(id)

        return jsonify(
            {
                "success": True,
                "message": "Deal fetched successfully",
                "data": deal.to_dict(),
            }
        ), HTTPStatus.OK
