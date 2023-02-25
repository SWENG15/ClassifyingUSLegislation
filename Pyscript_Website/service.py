"""This module provides the necessary connection with the backend for the service page"""
# Disable import error as service.py is in the same
# directory as service.py at runtime
# pylint: disable=import-error
import model as ml

# Once seperate states are added,
# this should be run when a state is selected,
# and each state's model should be remembered
classifier, vectorizer = ml.train_model('subject_dataset.csv')

def submit_bill(*_):
    """submit_bill runs when a new bill's text is submitted"""
    # Disable undefined variable as the class is defined at runtime
    # pylint: disable=undefined-variable
    text = Element("bill").element.value
    Element("bill").clear()
    if not text:
        Element('output').element.innerText = "Bill empty"
    else:
        subject = ml.predict_subject(classifier,vectorizer,text)
        Element('output').element.innerText = subject[0]
