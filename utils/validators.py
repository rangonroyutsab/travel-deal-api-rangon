def validate_input_data(data):
    """
    Validate travel deal input.
    Returns a dictionary of errors.
    If the dictionary is empty, the input is valid.
    """

    errors = {}

    required_fields = ["destination", "price", "platform", "rating", "travel_type"]
    allowed_travel_types = ["Budget", "Luxury", "Adventure", "Family"]

    for field in required_fields:
        if field not in data:
            errors[field] = f"{field} is required"

    if errors:
        return errors

    if not str(data["destination"]).strip():
        errors["destination"] = "Destination cannot be empty"

    if not isinstance(data["price"], (int)):
        errors["price"] = "Price must be a number"
    elif data["price"] < 0:
        errors["price"] = "Price must be a positive number"

    if not isinstance(data["rating"], (float, int)):
        errors["rating"] = "Rating must be a number"
    elif not 1 <= data["rating"] <= 5:
        errors["rating"] = "Rating must be a number between 1 and 5"

    if data["travel_type"] not in allowed_travel_types:
        errors["travel_type"] = (
            "Travel type must be Budget, Luxury, Adventure, or Family"
        )

    if not str(data["platform"]).strip():
        errors["platform"] = "Platform cannot be empty"

    return errors
