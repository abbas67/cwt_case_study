
import json

from flask import Flask, abort, request
import logging


from cwt_case_study.db_utils import new_engine, query_reviews, READ_SQL, create_new_review, CREATE_SQL, delete_reviews, DELETE_SQL
from cwt_case_study.utils import validate_clothing_id, validate_review_data, load_model

_logger = logging.getLogger(__name__)
engine = new_engine()
app = Flask(__name__)
model = load_model


@app.route("/api/v1/reviews/<clothing_id>", methods=['GET'])
def get(clothing_id):
    """
    Endpoint to get clothing reviews by ID.
    :param clothing_id:
    :return:
    """
    validated_clothing_id = validate_clothing_id(clothing_id)
    if not validated_clothing_id:
        abort(400)

    query_results = query_reviews(engine.connect(), READ_SQL, clothing_id=validated_clothing_id)
    if not query_results:
        abort(404)

    for result in query_results:
        result.pop('index', None)

    return json.dumps(query_results)


@app.route("/api/v1/reviews/", methods=['POST'])
def create():
    """
    Endpoint to add clothing reviews
    :return:
    """

    validated_review_data = validate_review_data(dict(request.form))
    if not validated_review_data:
        abort(400)

    create_new_review(engine.connect(), CREATE_SQL, **validated_review_data)

    return b'OK'


@app.route("/api/v1/reviews/<clothing_id>", methods=['DELETE'])
def delete(clothing_id):
    """
    Endpoint to delete clothing reviews
    :return:
    """
    validated_clothing_id = validate_clothing_id(clothing_id)
    if not validated_clothing_id:
        abort(400)

    delete_reviews(engine.connect(), DELETE_SQL, clothing_id=validated_clothing_id)

    return b'OK'


@app.route("/api/v1/inference/", methods=['GET'])
def inference():

    print(model)

    return b'foo'


if __name__ == '__main__':
    app.run(debug=True)
