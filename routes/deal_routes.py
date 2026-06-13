import logging

from flask import Blueprint
from flask import request

from services.deal_service import DealService


# Deal Blueprint
deal_bp = Blueprint("deals", __name__)


@deal_bp.route("/", methods=["POST"])
def create_deal():
    """
    create a new deal and store
    it in the database

    POST /deals
    """

    data = request.get_json()
    logging.info("Create deal request received")

    response = DealService.create_deal(data)

    return response


@deal_bp.route("/", methods=["GET"])
def get_all_deals():
    """
    fetch all deals

    GET /deals
    """

    logging.info("Get all deals request received")

    response = DealService.get_all()

    return response


@deal_bp.route("/search", methods=["GET"])
def search_deals():
    """
    search deals by query parameters

    GET /deals/search
    """

    logging.info("Search deals request received")

    # get the query parameters from the request
    data = request.args
    response = DealService.search_deals(data)

    return response


@deal_bp.route("/filter", methods=["GET"])
def filter_deals():
    """
    filter deals by budget

    GET /deals/filter
    """

    logging.info("Filter deals request received")

    data = request.args
    response = DealService.filter_deals(data)

    return response


@deal_bp.route("/sort", methods=["GET"])
def sort_deals():
    """
    sort deals by query parameters

    GET /deals/sort
    """

    logging.info("Sort deals request received")

    data = request.args
    response = DealService.sort_deals(data)

    return response


@deal_bp.route("/recent", methods=["GET"])
def get_recent_deals():
    """
    fetch recently viewed deals

    GET /deals/recent
    """

    logging.info("Get recently viewed deals request received")

    response = DealService.get_recent_deals()

    return response


@deal_bp.route("/<int:deal_id>", methods=["GET"])
def get_deal_by_id(deal_id):
    """
    fetch a deal by its id

    GET /deals/{deal_id}
    """

    logging.info("Get deal by id request received: %s", deal_id)

    response = DealService.get_by_id(deal_id)

    return response
