import env
import constants as const

import requests
import json

api_key = env.API_KEY
bill_id = const.example_vetoed

url = f"https://api.legiscan.com/?key={api_key}&op=getBill&id={bill_id}"

response = requests.get(url)
data = response.json()

filename = f"pulled_bills/bill_{bill_id}.json"
with open(filename, 'w') as f:
    json.dump(data, f)

print(f"Data written to file: {filename}")

#To be used for batch calls
#url = f"https://api.legiscan.com/?key={api_key}&op=getSearch&state=FL&keyword=status%3Apassed"
#url = f"https://api.legiscan.com/?key={api_key}&op=getSearch&state=FL&keyword=status%3Avetoed"
