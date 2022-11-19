import os
import unittest

import pandas as pd
from sqlalchemy import create_engine

from cwt_case_study.db_utils import query_reviews, READ_SQL, create_new_review, CREATE_SQL, delete_reviews, DELETE_SQL
from review_server import app

app.testing = True


class TestReviewServer(unittest.TestCase):
    MOCK_DATABASE = os.path.join(os.path.dirname(__file__), 'resources', 'mock_db.db')

    def setUp(self):
        self.mock_engine = create_engine(f"sqlite:///{self.MOCK_DATABASE}")
        pd.DataFrame(columns=['ClothingId',
                              'Age',
                              'Title',
                              'ReviewText',
                              'Rating',
                              'RecommendedIND',
                              'PositiveFeedbackCount',
                              'DivisionName',
                              'DepartmentName',
                              'ClassName'],
                     data=[
                         [1, 21, "title_1", "review_text_1", 1, 1, 1, "division_1",
                          "department_1", "class_1"],
                         [1, 22, "title_2", "review_text_2", 2, 2, 2, "division_2",
                          "department_2", "class_2"],
                         [3, 23, "title_3", "review_text_3", 3, 3, 3, "division_3",
                          "department_3", "class_3"]]).to_sql('reviews', con=self.mock_engine, if_exists="replace")

    def test_query_reviews(self):
        with self.mock_engine.connect() as dao:
            expected = [{'index': 0, 'ClothingId': 1, 'Age': 21, 'Title': 'title_1', 'ReviewText': 'review_text_1',
                         'Rating': 1, 'RecommendedIND': 1, 'PositiveFeedbackCount': 1,
                         'DivisionName': 'division_1', 'DepartmentName': 'department_1', 'ClassName': 'class_1'},

                        {'index': 1, 'ClothingId': 1, 'Age': 22, 'Title': 'title_2', 'ReviewText': 'review_text_2',
                         'Rating': 2, 'RecommendedIND': 2, 'PositiveFeedbackCount': 2,
                         'DivisionName': 'division_2', 'DepartmentName': 'department_2', 'ClassName': 'class_2'}
                        ]

            actual = query_reviews(dao, READ_SQL, clothing_id=1)
            self.assertEqual(expected, actual)

            actual = query_reviews(dao, READ_SQL, clothing_id=4)
            self.assertEqual([], actual)

    def test_create_review(self):

        with self.mock_engine.connect() as dao:

            insert_data = {'ClothingId': 5, 'Age': 21, 'Title': 'title_1', 'ReviewText': 'review_text_1',
                           'Rating': 1, 'RecommendedIND': 1, 'PositiveFeedbackCount': 1,
                           'DivisionName': 'division_1', 'DepartmentName': 'department_1', 'ClassName': 'class_1'}

            create_new_review(dao, CREATE_SQL, **insert_data)
            expected = [{'index': None, 'ClothingId': 5, 'Age': 21, 'Title': 'title_1', 'ReviewText': 'review_text_1',
                         'Rating': 1, 'RecommendedIND': 1, 'PositiveFeedbackCount': 1, 'DivisionName': 'division_1',
                         'DepartmentName': 'department_1', 'ClassName': 'class_1'}]

            actual = query_reviews(dao, READ_SQL, clothing_id=5)
            self.assertEqual(expected, actual)

    def test_delete_review(self):

        with self.mock_engine.connect() as dao:

            delete_reviews(dao, DELETE_SQL, clothing_id=1)
            actual = query_reviews(dao, READ_SQL, clothing_id=1)
            self.assertEqual([], actual)
