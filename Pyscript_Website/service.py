"""This module provides the necessary connection with the backend for the service page"""
# Disable import error as service.py is in the same
# directory as service.py at runtime
# pylint: disable=import-error
import model as ml

# Once seperate states are added,
# this should be run when a state is selected,
# and each state's model should be remembered
classifier, vectorizer = ml.train_model('subject_dataset.csv')

# Disable undefined variable as the class is defined at runtime
# pylint: disable=undefined-variable
submitted_bill = Element("bill")

def submit_bill():
    """submit_bill runs when a new bill's text is submitted"""
    print("Submitted succesfully \n")
    submitted_bill.clear()
    if not submitted_bill.element.value:
        print("Bill empty")
    else:
        print(ml.predict_subject(classifier,vectorizer,submitted_bill.element.value))
