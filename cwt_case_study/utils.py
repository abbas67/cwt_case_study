import logging
import pickle

_logger = logging.getLogger(__name__)

REQUIRED_FIELDS = {"ClothingId": int, "Age": int, "Title": str, "ReviewText": str, "Rating": int, "RecommendedIND": int, "PositiveFeedbackCount": int,
                   "DivisionName": str, "DepartmentName": str, "ClassName": str}


def validate_clothing_id(clothing_id) -> int:
    """
    :param clothing_id:
    :return:
    """
    _logger.info("Validating clothing ID.")
    if clothing_id and clothing_id.isdigit():
        return int(clothing_id)
    _logger.info("ID provided was not valid, abandoning...")


def validate_review_data(review_data) -> dict:
    """
    :param review_data:
    :return:
    """
    for field_name, data_type in REQUIRED_FIELDS.items():

        if field_name not in review_data:
            return {}
        if data_type == int:
            if review_data[field_name].isdigit():
                review_data[field_name] = int(review_data[field_name])
            else:
                return {}

    return review_data


def load_model():

    with open("model.pkl", "rb") as in_file:

        model = pickle.load(in_file)

    return model






