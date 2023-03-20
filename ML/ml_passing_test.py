"""This moudule tests the ML regression model defined in pass_model.py"""

import pass_model

MODEL_TRAINING_DATA_PATH = 'ETL_pipeline/datasets/west-virginia-dataset.csv'


def test_train_model():
    """This test confrims that training the model does not return null"""
    # Train model with test data
    clf, vectorizer = pass_model.train_model(
        training_data=MODEL_TRAINING_DATA_PATH)
    # Check that the classifier and vectorizer are not None
    assert clf is not None
    assert vectorizer is not None


def test_train_regression_model():
    "This test comfroms that training the model does not return null"
    # Train model with test data
    model, vectorizer = pass_model.train_regression_model(
        training_data=MODEL_TRAINING_DATA_PATH)

    # Check that the model and vectorizer are not None
    assert model is not None
    assert vectorizer is not None


def test_predict_pass():
    """This test checks that the model's predictions are correct"""
    with open('ML/test_data/pass_test1.txt', 'r', encoding="utf-8") as file:
        test_text_1 = file.read()

    with open('ML/test_data/pass_test2.txt', 'r', encoding="utf-8") as file:
        test_text_2 = file.read()

    with open('ML/test_data/pass_test3.txt', 'r', encoding="utf-8") as file:
        test_text_3 = file.read()

    with open('ML/test_data/veto_test1.txt', 'r', encoding="utf-8") as file:
        test_text_4 = file.read()

    with open('ML/test_data/veto_test2.txt', 'r', encoding="utf-8") as file:
        test_text_5 = file.read()

    with open('ML/test_data/veto_test3.txt', 'r', encoding="utf-8") as file:
        test_text_6 = file.read()
    # Train regression model with the data
    model, vectorizer = pass_model.train_regression_model(
        training_data=MODEL_TRAINING_DATA_PATH)

    # Predict pass or veto for test text
    pred1 = pass_model.predict_pass(model, vectorizer, test_text_1)
    pred2 = pass_model.predict_pass(model, vectorizer, test_text_2)
    pred3 = pass_model.predict_pass(model, vectorizer, test_text_3)
    pred4 = pass_model.predict_pass(model, vectorizer, test_text_4)
    pred5 = pass_model.predict_pass(model, vectorizer, test_text_5)
    pred6 = pass_model.predict_pass(model, vectorizer, test_text_6)

    pred6 = pass_model.predict_pass(model, vectorizer, test_text_6)

    # Check that the predicted subject is not None
    assert pred1 is not None
    assert pred2 is not None
    assert pred3 is not None
    assert pred4 is not None
    assert pred5 is not None
    assert pred6 is not None

    # Check the regressions model liklihood of passing percentage
    # First 3 tests with bills that have passed and last 3 with bills that were vetoed
    assert pred1 >= 0.9
    assert pred2 >= 0.9
    assert pred3 >= 0.9
    assert pred4 <= 0.1
    assert pred5 <= 0.1
    assert pred6 <= 0.1
