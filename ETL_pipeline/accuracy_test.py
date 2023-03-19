import pytest
from ..ML.subject_model import train_model_accuracy

test_data = [
    ("ETL_pipeline/datasets/west-virginia-dataset.csv",0.9)
] 

@pytest.mark.parametrize("a,expected",test_data)
def test_state_accuracy(a,expected):
    accuracy = train_model_accuracy(a)
    assert accuracy > expected

