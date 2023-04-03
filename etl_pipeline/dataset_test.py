"""
This module tests the quality of the dataset
    - Accuracy of the model it trains
    - Valid dataset
"""
import pytest
from ..etl_pipeline.analyse_dataset import analyse_data
from ..ML.subject_model import train_model_accuracy

# This is the number of times the accuracy is calculated for each dataset
# to find a better estimate of the accuracy
NUM_TESTS = 20

test_data = [
    ("etl_pipeline/datasets/west-virginia-dataset.csv",0.5)
    ("etl_pipeline/datasets/montana-dataset.csv",0.5)
]

state_list = [
    ("etl_pipeline/datasets/west-virginia-dataset.csv"),
    ("etl_pipeline/datasets/montana-dataset.csv")
]

@pytest.mark.parametrize("path,expected",test_data)
def test_state_accuracy(path,expected):
    """
    This function tests the accuracy of a dataset's model
    """
    total = 0
    for _ in range(0,NUM_TESTS):
        total += train_model_accuracy(path)

    accuracy = total/NUM_TESTS
    assert accuracy > expected

@pytest.mark.parametrize("path",state_list)
def test_state_validity(path):
    """
    This function tests if a states dataset is valid
    """
    subject_list = analyse_data(path)
    assert None not in subject_list
