"""This module tests the ML classification model defined in subject_model.py"""

import model

MODEL_TRAINING_DATA_PATH = 'ETL_pipeline/datasets/west-virginia-dataset.csv'

def test_train_model():
    """This test confirms that training the model does not return null"""
    # Train model with test data
    clf, vectorizer = model.train_model(training_data=MODEL_TRAINING_DATA_PATH)

    # Check that the classifier and vectorizer are not None
    assert clf is not None
    assert vectorizer is not None

def test_predict_subject():
    """This test checks that the model's classfications are correct"""
    with open('ML/test_data/test1.txt','r', encoding="utf-8") as file:
        test_text_1 = file.read()

    with open('ML/test_data/test2.txt','r', encoding="utf-8") as file:
        test_text_2 = file.read()

    with open('ML/test_data/test3.txt','r', encoding="utf-8") as file:
        test_text_3 = file.read()

    with open('ML/test_data/test4.txt','r', encoding="utf-8") as file:
        test_text_4 = file.read()

    with open('ML/test_data/test5.txt','r', encoding="utf-8") as file:
        test_text_5 = file.read()
    # Train model with test data
    clf, vectorizer = model.train_model(training_data=MODEL_TRAINING_DATA_PATH)


    # Predict subject for test text
    pred1 = model.predict_subject(clf, vectorizer, test_text_1)
    pred2 = model.predict_subject(clf, vectorizer, test_text_2)
    pred3 = model.predict_subject(clf, vectorizer, test_text_3)
    pred4 = model.predict_subject(clf, vectorizer, test_text_4)
    pred5 = model.predict_subject(clf, vectorizer, test_text_5)

    # Check that the predicted subject is not None
    assert pred1 is not None
    assert pred2 is not None
    assert pred3 is not None
    assert pred4 is not None
    assert pred5 is not None

    # Check model predicted correct subject

    #assert pred1 == 'Juvenile'
    #assert pred2 == 'Taxation'
    assert pred3 == 'Corrections'
    assert pred4 == 'Crime'
    assert pred5 == 'Health'
