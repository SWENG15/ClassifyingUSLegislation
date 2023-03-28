"""This module is used to clean dataset csvs"""

import csv
import re

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
    """Removes all bills that have no assigned subject, also standardise the subject matter"""
    csv.field_size_limit(100000000)
    # pylint: disable=line-too-long
    with open(filename + '.csv', 'r', encoding='UTF-8') as fin, open(filename + '_purged.csv', 'w', newline='', encoding='UTF-8') as fout:
        reader = csv.reader(fin, skipinitialspace=True)
        writer = csv.writer(fout, delimiter=',')
        writer.writerow(next(reader))
        for line in reader:
            if not line[-1] == "No Subject Provided":
                # For bills that have subject matter, simplify the subject e.g 'Legislature--Rule Making' becomes 'Legislature'
                subject_parts = line[-1].split('--')
                main_subject = subject_parts[0]
                if main_subject != line[-1]:
                    info = f"Simplified {line[-1]} to {main_subject}"
                    print(info)
                match = re.search(r"(.+)\(And Related Subheadings\)", main_subject)
                if match:
                    trimmed_part = match.group(1)
                    print(main_subject + " trimmed to: " + trimmed_part)
                    main_subject = trimmed_part
                line[-1] = main_subject.rstrip()
                writer.writerow(line)

#DO NOT INCLUDE .CSV FILE EXTENSION IN NAME, e.g enter "dataset" not "dataset.csv"
FILENAME = "datasets/west-virginia-dataset"
if __name__ == "__main__":
    #remove_blank_rows_csv(FILENAME)
    remove_no_subject_csv(FILENAME)
