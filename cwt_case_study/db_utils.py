"""
DB Util module for neatness.
"""
import logging
import os

from sqlalchemy import create_engine, text

_logger = logging.getLogger(__name__)

DATABASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'db', 'cwt_db.db')
DATABASE_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'Womens Clothing E-Commerce Reviews.csv')


def new_engine():
    """
    Creates a basic sqlalchemy engine object.
    :return: new engine object.
    """
    _logger.info("Generating new engine.")
    return create_engine(f"sqlite:///{DATABASE}")


def query_reviews(conn, sql, **query_params):
    """
    Executes query, all have homogenous inputs and outputs.
    :param conn:
    :param sql:
    :param query_params:
    :return: results of query.
    """
    _logger.info(f"Executing Query: {sql}")

    return [dict(row) for row in conn.execute(text(sql), query_params)]


def create_new_review(conn, sql, **query_params):
    """
    :param conn:
    :param sql:
    :param query_params:
    :return:
    """
    conn.execute(text(sql), query_params)


def delete_reviews(conn, sql, **query_params):
    """
    :param conn:
    :param sql:
    :param query_params:
    :return:
    """

    conn.execute(text(sql), query_params)


CREATE_SQL = f"""
INSERT INTO reviews(ClothingId, Age, Title, ReviewText, Rating, RecommendedIND, PositiveFeedbackCount, DivisionName, DepartmentName, ClassName)
VALUES(:ClothingId, :Age, :Title, :ReviewText, :Rating, :RecommendedIND, :PositiveFeedbackCount, :DivisionName, :DepartmentName, :ClassName)
"""

READ_SQL = f"""
SELECT * 
FROM reviews
WHERE ClothingId=:clothing_id
"""

DELETE_SQL = f"""
DELETE 
FROM reviews
WHERE ClothingId=:clothing_id
"""
