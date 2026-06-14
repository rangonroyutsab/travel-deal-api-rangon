ALLOWED_TRAVEL_TYPES = ["Budget", "Luxury", "Adventure", "Family"]
ALLOWED_SORT_FIELDS = ["destination", "price", "platform", "rating", "travel_type"]
ALLOWED_SORT_ORDERS = ["asc", "desc"]


def is_empty(value):
    """
    Check if a query value is empty.
    """

    return value is None or not str(value).strip()


def is_valid_number(value):
    """
    Check if a value can be converted to a number.
    """

    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def validate_input_data(data):
    """
    Validate travel deal input.
    Returns a dictionary of errors.
    If the dictionary is empty, the input is valid.
    """

    errors = {}

    if not isinstance(data, dict):
        errors["body"] = "Request body must be valid JSON"
        return errors

    required_fields = ["destination", "price", "platform", "rating", "travel_type"]

    for field in required_fields:
        if field not in data:
            errors[field] = f"{field} is required"

    if errors:
        return errors

    if not str(data["destination"]).strip():
        errors["destination"] = "Destination cannot be empty"

    if not isinstance(data["price"], (int, float)):
        errors["price"] = "Price must be a number"
    elif data["price"] < 0:
        errors["price"] = "Price must be a positive number"

    if not isinstance(data["rating"], (float, int)):
        errors["rating"] = "Rating must be a number"
    elif not 1 <= data["rating"] <= 5:
        errors["rating"] = "Rating must be a number between 1 and 5"

    if data["travel_type"] not in ALLOWED_TRAVEL_TYPES:
        errors["travel_type"] = (
            "Travel type must be Budget, Luxury, Adventure, or Family"
        )

    if not str(data["platform"]).strip():
        errors["platform"] = "Platform cannot be empty"

    return errors


def validate_search_query(data):
    """
    Validate search query parameters.
    Returns a dictionary of errors.
    """

    errors = {}
    search_fields = ["destination", "platform", "travel_type"]

    has_search_field = any(field in data for field in search_fields)

    if not has_search_field:
        errors["search"] = "At least one search parameter is required"
        return errors

    for field in search_fields:
        if field in data and is_empty(data.get(field)):
            errors[field] = f"{field} cannot be empty"

    if errors:
        return errors

    travel_type = data.get("travel_type")
    allowed_travel_types = [
        allowed_type.lower() for allowed_type in ALLOWED_TRAVEL_TYPES
    ]

    if travel_type and travel_type.lower() not in allowed_travel_types:
        errors["travel_type"] = (
            "Travel type must be Budget, Luxury, Adventure, or Family"
        )

    return errors


def validate_filter_query(data):
    """
    Validate budget filter query parameters.
    Returns a dictionary of errors.
    """

    errors = {}
    min_price = data.get("min_price")
    max_price = data.get("max_price")

    if is_empty(min_price) and is_empty(max_price):
        errors["price"] = "At least one price filter is required"
        return errors

    if not is_empty(min_price) and not is_valid_number(min_price):
        errors["min_price"] = "Minimum price must be a number"

    if not is_empty(max_price) and not is_valid_number(max_price):
        errors["max_price"] = "Maximum price must be a number"

    if errors:
        return errors

    if not is_empty(min_price) and float(min_price) < 0:
        errors["min_price"] = "Minimum price cannot be negative"

    if not is_empty(max_price) and float(max_price) < 0:
        errors["max_price"] = "Maximum price cannot be negative"

    if (
        not is_empty(min_price)
        and not is_empty(max_price)
        and float(max_price) < float(min_price)
    ):
        errors["max_price"] = "Maximum price cannot be smaller than minimum price"

    return errors


def validate_sort_query(data):
    """
    Validate sorting query parameters.
    Returns a dictionary of errors.
    """

    errors = {}
    sort_by = data.get("sort_by")
    order = data.get("order", "asc")

    if is_empty(sort_by):
        errors["sort_by"] = "Sort field is required"
    elif sort_by not in ALLOWED_SORT_FIELDS:
        errors["sort_by"] = "Invalid sort field"

    if is_empty(order):
        errors["order"] = "Sort order cannot be empty"
    elif order.lower() not in ALLOWED_SORT_ORDERS:
        errors["order"] = "Sort order must be asc or desc"

    return errors
