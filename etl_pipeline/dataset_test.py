"""
This module tests the quality of the dataset
    - Accuracy of the model it trains
    - Valid dataset
"""
import pytest
from ..etl_pipeline.analyse_dataset import analyse_data
from ..ML.subject_model import train_model_accuracy

test_data = [
    ("etl_pipeline/datasets/west-virginia-dataset.csv",0.5)
]

state_list = [
    ("etl_pipeline/datasets/west-virginia-dataset.csv")
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
