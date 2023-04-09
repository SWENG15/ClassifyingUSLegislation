"""
This module tests the quality of the dataset
    - Accuracy of the model it trains
    - Valid dataset
"""
import csv
import pytest
from ..etl_pipeline.analyse_dataset import analyse_data
from ..ML.subject_model import train_model_accuracy

test_data = [
    ("etl_pipeline/datasets/west-virginia-dataset.csv",0.5),
    ("etl_pipeline/datasets/tennessee-dataset.csv",0.5)
]

state_list = [
    ("etl_pipeline/datasets/west-virginia-dataset.csv"),
    ("etl_pipeline/datasets/alabama-dataset.csv"),
    ("etl_pipeline/datasets/tennessee-dataset.csv")
]

@pytest.mark.parametrize("path,expected",test_data)
def test_state_accuracy(path,expected):
    """
    This function tests the accuracy of a dataset's model
    """
    assert train_model_accuracy(path) > expected

@pytest.mark.parametrize("path",state_list)
def test_state_validity(path):
    """
    This function tests if a states dataset is valid
    """
    subject_list = analyse_data(path)
    assert None not in subject_list
    one_passed = False
    one_failed = False
    with open(path, 'r',  encoding='UTF-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)
        column_index = header.index('Status')
        for row in csv_reader:
            if 'Passed' in row[column_index]:
                one_passed = True
            elif 'Vetoed' in row[column_index] or 'Failed' in row[column_index]:
                one_failed = True
    assert one_passed is True
    assert one_failed is True
