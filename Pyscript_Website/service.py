"""This module provides the necessary connection with the backend for the service page"""
# Disable import error as service.py is in the same
# directory as service.py at runtime
# pylint: disable=import-error
import model as ml


# Pylint labels these as constants incorrectly
# pylint: disable=invalid-name
state, classifier, vectorizer = None, None, None
states = {}
remove_overlay()

def submit_bill(*_):
    """submit_bill runs when a new bill's text is submitted"""
    # Disable undefined variable as the class is defined at runtime
    # pylint: disable=undefined-variable
    text = Element("bill").element.value
    Element("bill").clear()
    if not text:
        Element('output').element.innerText = "Bill empty"
    else:
        if state is not None:
            subject = ml.predict_subject(classifier,vectorizer,text)
            Element('output').element.innerText = subject[0]
        else:
            Element('output').element.innerText = 'State not selected'

def choose_state(*_, new_state=None):
    """
    choose_state runs when a state is selected, 
    making sure the necessary ML model is available
    """
    # Need global variables because of how Pyscript works
    # pylint: disable=global-statement
    global state
    global classifier
    global vectorizer
    global states
    state, classifier, vectorizer, states = change_state(new_state, states)

def change_state(new_state, states_dict):
    """
    change state returns 
        - current state
        - ML classification model for that state
        - vectorizer for that state
        - the states -> classification/vectorizer dict

    given the new state value and the current states dictionary
    """
    # If the new state isn't passed, then reset the state to null
    if new_state is None:
        return None, None, None, states_dict

    # Case that new state is actually new
    if state != new_state:
        # If the model for this state has already been trained, use that model
        if new_state in states:
            new_classifier = states_dict[state][0]
            new_vectorizer = states_dict[state][1]

        # If the model for this state has not already been trained, train it
        # and add it to the dictionary of models
        else:
            new_classifier, new_vectorizer = ml.train_model(str(new_state)+'-dataset.csv')
            states[new_state] = (new_classifier,new_vectorizer)

    return new_state, new_classifier, new_vectorizer, states


def remove_overlay(): 
    Element('load_overlay').clear()
Element('load_overlay').remove_class("Load__screen__overlay")

remove_overlay()