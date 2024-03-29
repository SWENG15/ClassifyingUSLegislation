"""This module tests the ML classification model defined in subject_model.py"""
import subject_model
import pass_model
import bill_similarity_model

MODEL_TRAINING_DATA_PATH = 'etl_pipeline/datasets/west-virginia-dataset.csv'

def test_train_model():
    """This test confirms that training the model does not return null"""
    # Train model with test data
    clf, vectorizer = subject_model.train_model('west-virginia',
    training_data=MODEL_TRAINING_DATA_PATH)
    pass_model.train_regression_model('west-virginia', training_data=MODEL_TRAINING_DATA_PATH)
    bill_similarity_model.train_similarity_model('west-virginia',
                                                 training_data=MODEL_TRAINING_DATA_PATH)
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
    clf, vectorizer = subject_model.train_model('test', training_data=MODEL_TRAINING_DATA_PATH)


    # Predict subject for test text
    pred1 = subject_model.predict_subject(clf, vectorizer, test_text_1)
    pred2 = subject_model.predict_subject(clf, vectorizer, test_text_2)
    pred3 = subject_model.predict_subject(clf, vectorizer, test_text_3)
    pred4 = subject_model.predict_subject(clf, vectorizer, test_text_4)
    pred5 = subject_model.predict_subject(clf, vectorizer, test_text_5)

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
