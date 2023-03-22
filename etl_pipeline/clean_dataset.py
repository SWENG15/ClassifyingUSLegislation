"""This module is used to clean dataset csvs"""

import csv

def remove_blank_rows_csv(filename):
    """Removes blank rows from csvs leaving only data"""
    # pylint: disable=line-too-long
    with open(filename + ".csv","r", encoding='UTF-8') as infile, open(filename + "_cleaned.csv","w", encoding='UTF-8') as outfile:
        for line in infile.readlines():
            if not line.strip():
                continue
            if line:
                outfile.write(line)

def remove_no_subject_csv(filename):
    """Removes all bills that have no assigned subject"""
    csv.field_size_limit(100000000)
    # pylint: disable=line-too-long
    with open(filename + '.csv', 'r', encoding='UTF-8') as fin, open(filename + '_purged.csv', 'w', newline='', encoding='UTF-8') as fout:
        reader = csv.reader(fin, skipinitialspace=True)
        writer = csv.writer(fout, delimiter=',')
        writer.writerow(next(reader))
        for line in reader:
            if not line[-1] == "No Subject Provided":
                writer.writerow(i)

#DO NOT INCLUDE .CSV FILE EXTENSION IN NAME, e.g enter "dataset" not "dataset.csv"
FILENAME = "datasets/new-jersey-dataset"
if __name__ == "__main__":
    #remove_blank_rows_csv(FILENAME)
    remove_no_subject_csv(FILENAME)
