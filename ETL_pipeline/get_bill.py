"""This module is used to Extract, Transform and Load bill data."""

import json
import csv
import base64
from bs4 import BeautifulSoup
import requests
import env
from legiscan import LegiScan
import codes


def extract_bill_text(base64_enc):
    """Given a base64 encoded html document, return only the text"""
    doc_html = base64.b64decode(base64_enc)
    soup = BeautifulSoup(doc_html, "html.parser")
    content = soup.find('div', {'class':'document'})
    return content.text

#Create Legiscan API session
legis = LegiScan(env.API_KEY)

#Define Search
bills = legis.search(state='sc', query='status:passed')

#Create csv file and define its header columns
CSV_FILENAME = "dataset.csv"
header = ['ID', 'Title', 'Text', 'Status']
with open(CSV_FILENAME, 'w', encoding='UTF-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)

    #Populate csv file with each bill being one row
    for b in bills['results']:
        bill_id = b['bill_id']
        bill_title = b['title']

        print("Bill Title: " + str(bill_title))
        print("Bill ID: " + str(bill_id))

        #Write bill json
        url = f"https://api.legiscan.com/?key={env.API_KEY}&op=getBill&id={bill_id}"
        response = requests.get(url, timeout = 10)
        data = response.json()
        filename = f"pulled_bills/bill_{bill_id}.json"
        with open(filename, 'w', encoding='UTF-8') as f:
            json.dump(data, f)

        #Get bill status number and find text equivalent
        bill_status = codes.BILL_STATUS[data['bill']['status']]
        print("Bill Status: " + bill_status)

        #Find number of texts associated with bill and select most recent one
        num_texts = len(data['bill']['texts'])

        #Only write to csv if the text field won't be empty
        if num_texts > 0:
            bill_doc_id = data['bill']['texts'][num_texts - 1]['doc_id']
            print("Doc ID: " + str(bill_doc_id) + "\n")
            doc_text64 = legis.get_bill_text(bill_doc_id).get('doc')
            document_text = extract_bill_text(doc_text64)
            print(document_text)

            #Write all relevant bill information into csv
            csv_row = [bill_id, bill_title, document_text, bill_status]
            csvwriter.writerow(csv_row)
