"""This module is used to clean dataset csvs"""

import csv
import re

from analyse_dataset import analyse_data

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

def drop_rare_subjects(filename, occurences):
    """Removes all bills which have a subject that appears less than X times"""
    csv.field_size_limit(100000000)
    counts = analyse_data(filename + ".csv")[0]
    low_counts = []
    # pylint: disable=consider-using-dict-items
    for key in counts.keys():
        print(key + ": " + str(counts[key]))
        if counts[key] <= occurences:
            low_counts.append(key)
    # pylint: disable=line-too-long
    with open(filename + '.csv', 'r', encoding='UTF-8') as fin, open(filename + '_denoised.csv', 'w', newline='', encoding='UTF-8') as fout:
        reader = csv.reader(fin, skipinitialspace=True)
        writer = csv.writer(fout, delimiter=',')
        writer.writerow(next(reader))
        for line in reader:
            if  line[-1] not in low_counts:
                writer.writerow(line)

#DO NOT INCLUDE .CSV FILE EXTENSION IN NAME, e.g enter "dataset" not "dataset.csv"
FILENAME = "datasets/louisiana-dataset"
if __name__ == "__main__":
    #remove_blank_rows_csv(FILENAME)
    #remove_no_subject_csv(FILENAME)
    drop_rare_subjects(FILENAME,5)
