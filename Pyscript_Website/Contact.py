"""
This module contains a function for submitting a contact form.

The submit_contact_form function takes in any number of arguments and keyword arguments, 
but it is designed to work with an Element object that has an 'email' attribute. If the 'email' 
attribute is not empty, the function sends a message to confirm that the form has been submitted 
and a response will be sent to the provided email address.
"""
from elements import Element

def submit_contact_form(*args, **kwargs):
    message = Element('form_recieved')
    if Element('email').value != "":
        message.write(f"Request sent, you will recieve a "
                     "response to {Element('email').value} shortly")
        