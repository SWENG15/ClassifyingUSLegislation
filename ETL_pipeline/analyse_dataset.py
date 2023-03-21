"""This module is used to test the properties of a dataset"""
#pylint: disable=invalid-name
import codecs
import csv
import sys
import pandas as pd

max_int = sys.maxsize
while True:
    try:
        csv.field_size_limit(max_int)
        break
    except OverflowError:
        max_int = int(max_int/10)

with codecs.open("ETL_pipeline/datasets/west-virginia-dataset.csv", 'r', encoding='Latin1') as file:
    reader = csv.reader(file)
    data = pd.DataFrame(reader, columns=['ID', 'title', 'text', 'status', 'subject'])

data.drop('ID', axis=1)
data.drop('title',axis=1)
data.drop('text',axis=1)
data.drop('status',axis=1)

subject_counts = {}

for _, row in data.iterrows():
    subject = row['subject']
    if subject not in subject_counts:
        subject_counts[subject] = 1
    else:
        subject_counts[subject] += 1

sorted_subjects = dict(sorted(subject_counts.items(), key=lambda x:x[1]))

print(sorted_subjects)
print(f"Total number of subject matters: {len(data)}")
