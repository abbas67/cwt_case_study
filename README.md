# cwt_case_study

**Setting up the server**

1. install the requirements in requirements.txt.
2. Run load_data.py. 
3. run review_server.py

Didn't have time to implement the inference endpoint but essentially, I would use the get_model function to get the model and reuse it as needed, by passing in lists of tuples into the predict_proba function.

**Endpoints**

/api/v1/reviews/<clothing_id> GET to retrieve reviews by ID.

/api/v1/reviews/<clothing_id> DELETE to delete reviews by ID.

/api/v1/reviews/ POST to create (send create data in body in json format.)

e.g. 

{
    "ClothingId": 5,
    "Age": 21,
    "Title": "title_1",
    "ReviewText": "review_text_1",
    "Rating": 1,
    "RecommendedIND": 1,
    "PositiveFeedbackCount": 1,
    "DivisionName": "division_1",
    "DepartmentName": "department_1",
    "ClassName": "class_1"
}