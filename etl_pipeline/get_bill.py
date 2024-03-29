"""This module is used to Extract, Transform and Load bill data."""

import csv
import base64
from io import StringIO
import re
import os
# pylint: disable=import-error
from bs4 import BeautifulSoup
from bs4.element import Comment
from PyPDF2 import PdfReader
import requests
from ..etl_pipeline.env import API_KEY
from ..etl_pipeline.legiscan import LegiScan
from ..etl_pipeline.codes import BILL_STATUS

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
    filename = f"doc_{doc_id}.pdf"
    with open(filename,'wb') as file:
        file.write(text)
    return filename

def read_pdf_text(filename):
    """Return text from pdf document, cleaning line numbers"""
     # creating a pdf reader object
    reader = PdfReader(filename)
    output_text = ''
    # pylint: disable=consider-using-enumerate
    for index in range(len(reader.pages)):
        page = reader.pages[index]
        text = page.extract_text()

        # Remove line numbers
        lines = StringIO(text).readlines()
        text = ''.join([re.sub(r'^\d+\s+', '', line) for line in lines])

        output_text += text
    print(output_text)

    return output_text

#Create Legiscan API session
legis = LegiScan(API_KEY)


#Define Search
QUERY_STATE = 'nj'
SEARCH_QUERY = 'the'
#Define Search
#QUERY_STATE = 'wv'
#SEARCH_QUERY = 'and'

# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
def get_bills_from_search(query_state, search_query, csv_name, num_pages, legi_env):
    """Given a search state and query, produce a csv file of the relevant information"""
    #Make a list of already pulled bills to avoid duplicates
    already_pulled = []
    if csv_name == "pytest.csv":
        already_pulled = []
    else:
        with open('already_pulled.txt', 'r+', encoding='UTF-8') as pulled:
            contents = pulled.read()
            already_pulled = contents.split()
    print(already_pulled)
    csv_filename = csv_name
    header = ['ID', 'Title', 'Text', 'Status', 'Subject']
    with open(csv_filename, 'a+', encoding='UTF-8',newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(header)
        # pylint: disable=too-many-nested-blocks
        for page_index in range(num_pages):
            bills = legi_env.search(state=query_state, query=search_query, page=page_index)
            #Populate csv file with each bill being one row
            # pylint: disable=invalid-name
            for b in bills['results']:
                bill_id = b['bill_id']
                print("Bill ID: " + str(bill_id))

                if str(bill_id) in already_pulled:
                    print("This bill has already been pulled.")
                else:
                    if csv_name != "pytest.csv":
                        with open('already_pulled.txt', 'a', encoding='utf-8') as f:
                            f.write(" " + str(bill_id))
                    #Write bill json
                    url = f"https://api.legiscan.com/?key={API_KEY}&op=getBill&id={bill_id}"
                    response = requests.get(url, timeout = 10)
                    data = response.json()
                    bill_title = data['bill']['title']
                    print("Bill Title: " + str(bill_title))

                    #Get bill status number and find text equivalent
                    bill_status = "No status"
                    if data['bill']['status'] == 0:
                        print("No status")
                    else:
                        bill_status = BILL_STATUS[data['bill']['status']]
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
                        bill_subject = "No Subject Provided"
                        if num_subjects > 0:
                        #Get bill subject matter
                            bill_subject = data['bill']['subjects'][0]['subject_name']
                            #Clean bill subject
                            subject_parts = bill_subject.split('--')
                            main_subject = subject_parts[0]
                            match = re.search(r"(.+)\(And Related Subheadings\)", main_subject)
                            if match:
                                trimmed_part = match.group(1)
                                main_subject = trimmed_part
                            bill_subject = main_subject.rstrip()
                            print("Bill Subject: " + str(bill_subject))
                            #Write all relevant bill information into csv
                            csv_row=[bill_id, bill_title, document_text, bill_status, bill_subject]
                            csvwriter.writerow(csv_row)
                        else:
                            print("No Bill Subject - Not writing")
                    else:
                        print("No texts")



if __name__ == "__main__":
    get_bills_from_search(QUERY_STATE, SEARCH_QUERY, "dataset.csv", 194, legis)
