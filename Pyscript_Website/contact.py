"""
This module contains a function for submitting a contact form.

The submit_contact_form function takes in any number of arguments and keyword arguments, 
but it is designed to work with an Element object that has an 'email' attribute. If the 'email' 
attribute is not empty, the function sends a message to confirm that the form has been submitted 
and a response will be sent to the provided email address.
"""


def submit_contact_form(*_):
    """
    This function is called when the contact form is submitted.
    It gives a message to the user saying the email has been sent.
    """
    # Disable undefined variable as the class is defined at runtime
    # pylint: disable=undefined-variable
    message = Element('form_recieved')
    email = Element('email').value
    if email != "":
        message.write(f"Request sent, you will receive a response to {email} shortly")
        