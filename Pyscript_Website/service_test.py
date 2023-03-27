"""This module tests the backend functionality for the Service page"""
import shutil
import os
import pytest

# Disable errors for importing outside top level
# as the imports need to happen after the setup function
# pylint: disable=import-outside-toplevel
@pytest.fixture(autouse=True)
def setup_and_teardown():
    """
    This function provides setup and teardown code which are run before and after the tests have run
    These set up the environment more similarly to how it will be set up at runtime.
    """
    # These need to be copied in the same way they are at runtime by pyscript
    shutil.copy("ML/subject_model.py","Pyscript_Website/subject_model.py")
    shutil.copy("etl_pipeline/datasets/west-virginia-dataset.csv","west-virginia-dataset.csv")
    yield
    os.remove("Pyscript_Website/subject_model.py")
    os.remove("west-virginia-dataset.csv")

def test_change_state_none():
    """This function tests change_state when the input is None"""
    import service
    assert service.change_state(None,{})==(None,None,None,None,None,{})

def test_change_state():
    """This function tests change_state when there is an input"""
    import service
    state,_,_,_,_,states= service.change_state("west-virginia",{})
    assert state=="west-virginia"
    assert "west-virginia" in states
