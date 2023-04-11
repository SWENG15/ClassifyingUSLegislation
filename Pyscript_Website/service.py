"""This module provides the necessary connection with the backend for the service page"""
# Disable import error as service.py is in the same
# directory as service.py at runtime
# pylint: disable=import-error
import subject_model as ml
import pass_model as pml
import bill_similarity_model as bsm
import threading
import time

# Pylint labels these as constants incorrectly
# pylint: disable=invalid-name
state = None
classifier, subject_vectorizer = None, None
pass_model, pass_vectorizer = None, None
similarity_model = None
states = {}

def submit_bill(*_):
    """submit_bill runs when a new bill's text is submitted"""
    # Disable undefined variable as the class is defined at runtime
    # pylint: disable=undefined-variable
    # pylint: disable=line-too-long
    text = Element("bill").element.value
    Element("bill").clear()
    if not text:
        Element('output').element.innerText = "Bill empty"
    else:
        if state is not None:
            subject = ml.predict_subject(classifier,subject_vectorizer,text)
            print('subject fine\n')
            pass_prob = pml.predict_pass(pass_model,pass_vectorizer,text)
            print('prob fine\n')
            similar_bills = bsm.predict_similar_bills(text, similarity_model)
            print('sim fine\n')
            output = f"Subject: {subject[0]}, Probability of passing: {pass_prob}, Similar bills: {similar_bills}"
            Element('output').element.innerText = output
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
    global subject_vectorizer
    global pass_model
    global pass_vectorizer
    global similarity_model
    global states
    # pylint: disable=line-too-long
    state, classifier, subject_vectorizer, pass_model, pass_vectorizer, similarity_model, states = change_state(new_state, states)

def change_state(new_state, states_dict):
    """
    change state returns 
        - current state
        - ML classification model for that state
        - subject_vectorizer for that state
        - pass model for that state
        - pass vectorizer for that state
        - the full similarity model for that state
        - the states -> classification/subject_vectorizer/pass_model/pass_vectorizer dict

    given the new state value and the current states dictionary
    """
    # If the new state isn't passed, then reset the state to null
    if new_state is None:
        return None, None, None, None, None, None, states_dict

    new_classifier, new_subject_vectorizer = ml.load_model(new_state)
    print('subject fine\n')
    new_pmodel, new_pvectorizer = pml.load_model(new_state)
    print('probability fine\n')
    new_sim_model = bsm.load_model(new_state)
    print('similar fine\n')
    # Case that new state is actually new
    #if state != new_state:
        # If the model for this state has already been trained, use that model
      #  if new_state in states:
       #     new_classifier = states_dict[state][0]
        #    new_subject_vectorizer = states_dict[state][1]
         #   new_pmodel = states_dict[state][2]
          #  new_pvectorizer = states_dict[state][3]
           # new_sim_model = states_dict[state][4]

        # If the model for this state has not already been trained, train it
        # and add it to the dictionary of models
        #else:
         #   new_classifier, new_subject_vectorizer = ml.train_model(str(new_state)+'-dataset.csv')
          #  new_pmodel, new_pvectorizer = pml.train_regression_model(str(new_state)+'-dataset.csv')
           # print('probability fine\n')
            #new_sim_model = bsm.train_similarity_model(str(new_state)+'-dataset.csv')
            #states[new_state] = (
             #   new_classifier,new_subject_vectorizer,new_pmodel,new_pvectorizer,new_sim_model
            #)"""
    # pylint: disable=line-too-long
    return new_state, new_classifier, new_subject_vectorizer, new_pmodel, new_pvectorizer, new_sim_model, states


def remove_overlay(): 
    Element('load_overlay').clear()
    Element('load_overlay').remove_class("Load__screen__overlay")
    stop_flag = True


remove_overlay()

