import logging
import os
import pickle

_logger = logging.getLogger(__name__)

REQUIRED_FIELDS = {"ClothingId": int, "Age": int, "Title": str, "ReviewText": str, "Rating": int, "RecommendedIND": int,
                   "PositiveFeedbackCount": int, "DivisionName": str, "DepartmentName": str, "ClassName": str}


def validate_clothing_id(clothing_id):
    """
    Basic QC to check the ID is provided and is a digit.
    :param clothing_id:
    :return: validated and converted clothing_id.
    """
    _logger.info("Validating clothing ID.")
    if clothing_id and clothing_id.isdigit():
        return int(clothing_id)
    _logger.info("ID provided was not valid, abandoning...")


def validate_review_data(review_data):
    """
    Basic QC to check if all the required fields are provided, along with their correct types.
    :param review_data:
    :return: validated and converted review data.
    """
    _logger.info("Validating review data...")
    for field_name, data_type in REQUIRED_FIELDS.items():
        if field_name not in review_data:
            _logger.info("missing field, abandoning.")
            return {}

        if data_type == int:
            if review_data[field_name].isdigit():
                review_data[field_name] = int(review_data[field_name])
            else:
                _logger.info(f"Incorrect data type provided for field: {field_name}")
                return {}

    return review_data


def load_model():
    """
    Loads the Model from file and returns it.
    :return:
    """
    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'model.pkl'), "rb") as in_file:

        model = pickle.load(in_file)

    return model




