"""This module is used to Extract, Transform and Load bill data."""

import csv
import base64
from io import StringIO
import re
import os
# pylint: disable=import-error
from bs4 import BeautifulSoup
from bs4.element import Comment
from PyPDF4 import PdfReader
import requests
import env
from legiscan import LegiScan
import codes



#Used for states with non-standard formatting
def tag_visible(element):
    """Used to detect which text is visible on a page"""
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def extract_bill_text(base64_enc,state):
    """Given a base64 encoded html document, return only the text"""
    doc_html = base64.b64decode(base64_enc)
    soup = BeautifulSoup(doc_html, "html.parser")
    #States that use standard formatting (List will be expanded from sc in future)
    if state == 'sc':
        content = soup.find('div', {'class':'document'})
        return content.text
    texts = soup.findAll(string=True)
    visible_texts = filter(tag_visible, texts)
    return " ".join(t.strip() for t in visible_texts)

def extract_bill_text_to_pdf(base64_enc, doc_id):
    """Given a base64 encoded pdf document, return the name of the file text has been written to"""
    text = base64.b64decode(base64_enc)
    filename = f"pulled_bills/doc_{doc_id}.pdf"
    with open(filename,'wb') as file:
        file.write(text)
    return filename

def read_pdf_text(filename):
    """Return text from pdf document, cleaning line numbers"""
     # creating a pdf reader object
    reader = PdfReader(filename)
    output_text = ''
    # pylint: disable=consider-using-enumerate
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        text = page.extract_text()

        # Remove line numbers
        lines = StringIO(text).readlines()
        text = ''.join([re.sub(r'^\d+\s+', '', line) for line in lines])

        output_text += text
    print(output_text)

    return output_text

#Create Legiscan API session
legis = LegiScan(env.API_KEY)

#Define Search
QUERY_STATE = 'al'
SEARCH_QUERY = 'the'

# pylint: disable=too-many-locals
def get_bills_from_search(query_state, search_query, csv_name, num_pages, legi_env):
    """Given a search state and query, produce a csv file of the relevant information"""
    csv_filename = csv_name
    header = ['ID', 'Title', 'Text', 'Status', 'Subject']
    with open(csv_filename, 'w', encoding='UTF-8') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(header)
        for page_index in range(num_pages):
            bills = legi_env.search(state=query_state, query=search_query, page=page_index)
            #Populate csv file with each bill being one row
            # pylint: disable=invalid-name
            for b in bills['results']:
                print(b)
                bill_id = b['bill_id']

                print("Bill ID: " + str(bill_id))

                #Write bill json
                url = f"https://api.legiscan.com/?key={env.API_KEY}&op=getBill&id={bill_id}"
                response = requests.get(url, timeout = 10)
                data = response.json()
                bill_title = data['bill']['title']
                print("Bill Title: " + str(bill_title))

                #Get bill status number and find text equivalent
                if data['bill']['status'] == 0:
                    print("No status")
                    continue
                bill_status = codes.BILL_STATUS[data['bill']['status']]
                print("Bill Status: " + bill_status)

                #Find number of texts associated with bill and select most recent one
                num_texts = len(data['bill']['texts'])

                #Only write to csv if the text field won't be empty
                if num_texts > 0:
                    bill_doc_id = data['bill']['texts'][num_texts - 1]['doc_id']
                    print("Doc ID: " + str(bill_doc_id) + "\n")
                    doc = legi_env.get_bill_text(bill_doc_id)
                    doc_text64 = doc.get('doc')

                    # If it is a pdf
                    if doc['mime'] == "application/pdf":
                        filename = extract_bill_text_to_pdf(doc_text64, bill_doc_id)
                        print(f"New pdf stored in {filename}")
                        # Get the text from the saved pdf into document_text
                        document_text = read_pdf_text(filename)
                        # Delete the saved pdf
                        os.remove(filename)
                        print("File Deleted successfully")
                    # check here instead if it is a html file
                    else:
                        document_text = "\"" + extract_bill_text(doc_text64, QUERY_STATE) + "\""
                        print(document_text)

                    num_subjects = len(data['bill']['subjects'])
                    # pylint: disable=invalid-name
                    bill_subject = "No Subject Provided"
                    if num_subjects > 0:
                    #Get bill subject matter
                        bill_subject = data['bill']['subjects'][0]['subject_name']
                        print("Bill Subject: " + str(bill_subject))
                    else:
                        print("No Bill Subject")

                    #Write all relevant bill information into csv
                    csv_row = [bill_id, bill_title, document_text, bill_status, bill_subject]
                    csvwriter.writerow(csv_row)

if __name__ == "__main__":
    get_bills_from_search(QUERY_STATE, SEARCH_QUERY, "dataset.csv", 4, legis)
