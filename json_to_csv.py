import pandas as pd
import constants as const

bill_id = const.example_vetoed
filename = f"pulled_bills/bill_{bill_id}.json"

df = pd.read_json(filename)
df.to_csv(f'pulled_bills/bill_{bill_id}.csv')
