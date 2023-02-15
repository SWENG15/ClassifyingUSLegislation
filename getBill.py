import json
import env
from legiscan import LegiScan
from bs4 import BeautifulSoup
import requests
import base64


#Given a base 64 encoded html document, return only the text
def extract_bill_text(base64_enc):
    doc_html = base64.b64decode(doc_text64)
    soup = BeautifulSoup(doc_html, "html.parser")
    content = soup.find('div', {'class':'document'})
    print(content.text)
    return doc_html

#Create Legiscan API sessions
legis = LegiScan(env.API_KEY)

#Define search
bills = legis.search(state='sc', query='status:passed')
bills['summary']

for b in bills['results']:
    bill_id = b['bill_id']
    bill_text_url = b['text_url']

    print("Bill ID: " + str(bill_id))

    #Write bill jsons
    url = f"https://api.legiscan.com/?key={env.API_KEY}&op=getBill&id={bill_id}"
    response = requests.get(url)
    data = response.json()
    filename = f"pulled_bills/bill_{bill_id}.json"
    with open(filename, 'w') as f:
        json.dump(data, f)
    print(f"Data written to file: {filename}")

    #Find number of texts and select most recent one
    num_texts = len(data['bill']['texts'])
    if(num_texts > 0):
        bill_doc_id = data['bill']['texts'][num_texts - 1]['doc_id']
        doc_text64 = legis.get_bill_text(bill_doc_id).get('doc')
        document_text = extract_bill_text(doc_text64)
        
    print("Bill Text URL: " + str(bill_text_url))
    print("Doc ID: " + str(bill_doc_id) + "\n")


