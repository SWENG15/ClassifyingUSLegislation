"""This module is used to test the properties of a dataset"""
#pylint: disable=invalid-name
#pylint: disable=duplicate-code
#pylint: disable=duplicate-code
import codecs
import csv
import sys
import pandas as pd

def analyse_data(data):
    """This function returns the a dictionary of the subjects in a dataset 
    with the number of times they appear, 
    as well as the total number of (non-unique) subjects in the dataset"""
    max_int = sys.maxsize
    while True:
        try:
            csv.field_size_limit(max_int)
            break
        except OverflowError:
            max_int = int(max_int/10)

    with codecs.open(data, 'r', encoding='Latin1') as file:
        reader = csv.reader(file)
        data = pd.DataFrame(reader, columns=['ID', 'title', 'text', 'status', 'subject'])

    data.drop('ID', axis=1)
    data.drop('title',axis=1)
    data.drop('text',axis=1)

    subject_counts = {}
    status_counts = {}

    for _, row in data.iterrows():
        subject = row['subject']
        if subject not in subject_counts:
            subject_counts[subject] = 1
        else:
            subject_counts[subject] += 1

        status = row['status']
        if status not in status_counts:
            status_counts[status] = 1
        else:
            status_counts[status] += 1

    sorted_subjects = dict(sorted(subject_counts.items(), key=lambda x:x[1]))

    return sorted_subjects, len(data)
    #print(status_counts)
