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

    response = DealService.create_deal(data)

    return response


@deal_bp.route("/", methods=["GET"])
def get_all_deals():
    """
    fetch all deals
    
    GET /deals
    """

    response = DealService.get_all()

    return response

@deal_bp.route("/<int:deal_id>", methods=["GET"])
def get_deal_by_id(deal_id):
    """
    fetch a deal by its id 

    GET /deals/{deal_id}
    """

    response = DealService.get_by_id(deal_id)

    return response

    

    


    
     
