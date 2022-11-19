import json
import unittest
from unittest import mock

from cwt_case_study.db_utils import CREATE_SQL, DELETE_SQL
from review_server import app

app.testing = True


class TestReviewServer(unittest.TestCase):

    @mock.patch("review_server.query_reviews")
    def test_get_review(self, mock_query_reviews):
        mock_query_reviews.side_effect = [[{'index': 22742, 'ClothingId': 1, 'Age': 50, 'Title': 'title_1',
                                            'ReviewText': "review_1", 'Rating': 5, 'RecommendedIND': 1,
                                            'PositiveFeedbackCount': 0, 'DivisionName': 'Intimates',
                                            'DepartmentName': 'Intimate', 'ClassName': 'Layering'},

                                           {'index': 22743, 'ClothingId': 1, 'Age': 36,
                                            'Title': 'Staple tank!', 'ReviewText': "review_2",
                                            'Rating': 5, 'RecommendedIND': 1,
                                            'PositiveFeedbackCount': 0, 'DivisionName': 'Initmates',
                                            'DepartmentName': 'Intimate', 'ClassName': 'Layering'}
                                           ], []]

        with app.test_client() as client:
            actual = client.get('/api/v1/reviews/1')
            expected = [{'ClothingId': 1, 'Age': 50, 'Title': 'title_1',
                         'ReviewText': "review_1", 'Rating': 5, 'RecommendedIND': 1,
                         'PositiveFeedbackCount': 0, 'DivisionName': 'Intimates',
                         'DepartmentName': 'Intimate', 'ClassName': 'Layering'},

                        {'ClothingId': 1, 'Age': 36,
                         'Title': 'Staple tank!', 'ReviewText': "review_2",
                         'Rating': 5, 'RecommendedIND': 1,
                         'PositiveFeedbackCount': 0, 'DivisionName': 'Initmates',
                         'DepartmentName': 'Intimate', 'ClassName': 'Layering'}
                        ]

            self.assertEqual(200, actual.status_code)
            self.assertEqual(expected, json.loads(actual.data.decode()))

            actual = client.get('/api/v1/reviews/2')
            self.assertEqual(404, actual.status_code)

            actual = client.get('/api/v1/reviews/one')
            self.assertEqual(400, actual.status_code)

            actual = client.get('/api/v1/reviews/null')
            self.assertEqual(400, actual.status_code)

    @mock.patch("review_server.create_new_review")
    def test_create_review(self, mock_create_review):
        data = {'ClothingId': 1, 'Age': 50, 'Title': 'title_1',
                'ReviewText': "review_1", 'Rating': 5, 'RecommendedIND': 1,
                'PositiveFeedbackCount': 0, 'DivisionName': 'Intimates',
                'DepartmentName': 'Intimate', 'ClassName': 'Layering'}

        with app.test_client() as client:
            response = client.post('/api/v1/reviews/', data=data)
            self.assertEqual(200, response.status_code)
            self.assertEqual(CREATE_SQL, mock_create_review.call_args[0][1])

            self.assertEqual(data, mock_create_review.call_args[1])

            response = client.post('/api/v1/reviews/', data={'ClothingId': 1, 'Age': "fifty", 'Title': 'title_1',
                                                             'ReviewText': "review_1", 'Rating': 5, 'RecommendedIND': 1,
                                                             'PositiveFeedbackCount': 0, 'DivisionName': 'Intimates',
                                                             'DepartmentName': 'Intimate', 'ClassName': 'Layering'})
            self.assertEqual(400, response.status_code)

            response = client.post('/api/v1/reviews/', data={'ClothingId': 1, 'Age': 50, 'Title': 'title_1',
                                                             'ReviewText': "review_1", 'RecommendedIND': 1,
                                                             'PositiveFeedbackCount': 0, 'DivisionName': 'Intimates',
                                                             'DepartmentName': 'Intimate', 'ClassName': 'Layering'})
            self.assertEqual(400, response.status_code)

    @mock.patch("review_server.delete_reviews")
    def test_delete_reviews(self, mock_delete_reviews):

        with app.test_client() as client:

            actual = client.delete('/api/v1/reviews/1')
            self.assertEqual(200, actual.status_code)

            actual = client.delete('/api/v1/reviews/one')
            self.assertEqual(400, actual.status_code)

            actual = client.delete('/api/v1/reviews/null')
            self.assertEqual(400, actual.status_code)

            self.assertEqual(DELETE_SQL, mock_delete_reviews.call_args[0][1])
            self.assertEqual({'clothing_id': 1}, mock_delete_reviews.call_args[1])


