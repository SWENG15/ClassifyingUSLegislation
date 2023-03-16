import time

def submit_contact_form(*args, **kwargs):
    message = Element('form_recieved')
    if(Element('email').value != ""):
        message.write(f"Request sent, you will recieve a response to {Element('email').value} shortly")
    
        