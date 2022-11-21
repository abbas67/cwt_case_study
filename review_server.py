
import json
from flask import Flask, abort, request
import logging

from cwt_case_study.db_utils import new_engine,  READ_SQL, CREATE_SQL, DELETE_SQL, execute_query, READ, CREATE, DELETE
from cwt_case_study.utils import validate_clothing_id, validate_review_data, load_model

_logger = logging.getLogger(__name__)
engine = new_engine()
app = Flask(__name__)
model = load_model()


@app.route("/api/v1/reviews/<clothing_id>", methods=['GET'])
def get(clothing_id):
    """
    Endpoint to get clothing reviews by ID.
    :param clothing_id:
    :return: server response.
    """
    _logger.info("get requested received.")
    validated_clothing_id = validate_clothing_id(clothing_id)
    if not validated_clothing_id:
        abort(400)

    query_results = execute_query(engine.connect(), READ_SQL, READ, clothing_id=validated_clothing_id)
    if not query_results:
        abort(404)

    for result in query_results:
        result.pop('index', None)

    _logger.info("Processing complete, returning response...")
    return json.dumps(query_results)


@app.route("/api/v1/reviews/", methods=['POST'])
def create():
    """
    Endpoint to add clothing reviews
    :return: server response.
    """
    _logger.info("Create requested received.")
    validated_review_data = validate_review_data(dict(request.form))
    if not validated_review_data:
        abort(400)

    execute_query(engine.connect(), CREATE_SQL, CREATE, **validated_review_data)

    _logger.info("Processing complete, returning response...")
    return b'OK'


@app.route("/api/v1/reviews/<clothing_id>", methods=['DELETE'])
def delete(clothing_id):
    """
    Endpoint to delete clothing reviews
    :return: server response.
    """
    _logger.info("Delete requested received.")
    validated_clothing_id = validate_clothing_id(clothing_id)
    if not validated_clothing_id:
        abort(400)

    execute_query(engine.connect(), DELETE_SQL, DELETE, clothing_id=validated_clothing_id)
    _logger.info("Processing complete, returning response...")
    return b'OK'


if __name__ == '__main__':
    app.run(port=3000)
