def format_response(status, message, data=None):
    """
    Helper function to standardize API responses.
    """
    return {
        "status": status,
        "message": message,
        "data": data
    }
