import pytest
from ..ETL_pipeline.analyse_dataset import analyse_data
from ..ML.subject_model import train_model_accuracy

# This is the number of times the accuracy is calculated for each dataset 
# to find a better estimate of the accuracy
NUM_TESTS = 20 

test_data = [
    ("ETL_pipeline/datasets/west-virginia-dataset.csv",0.5)
] 

state_list = [
    ("ETL_pipeline/datasets/west-virginia-dataset.csv"),
    ("ETL_pipeline/datasets/new-jersey-dataset.csv"),
    ("ETL_pipeline/datasets/alabama-dataset.csv")
]

@pytest.mark.parametrize("a,expected",test_data)
def test_state_accuracy(a,expected):
    sum = 0
    for _ in range(0,NUM_TESTS):
        sum += train_model_accuracy(a)
    
    accuracy = sum/NUM_TESTS
    assert accuracy > expected

@pytest.mark.parametrize("a",state_list)
def test_state_validity(a):
    subject_list = analyse_data(a)
    assert None not in subject_list
