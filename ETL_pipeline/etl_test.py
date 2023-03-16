"""This module tests the backend functionality for the Service page"""
import os
import get_bill
from legiscan import LegiScan
# pylint: disable=import-error
import env
import PyPDF2

def test_bill_extraction():
    """This function tests change_state when there is an input"""
    legis = LegiScan(env.API_KEY)
    test_fname = "pytest.csv"
    get_bill.get_bills_from_search("al", "specific+query", test_fname, 2, legis)
    #Test that csv was created
    assert os.path.exists(test_fname) is True
    with open(test_fname, 'r', encoding='UTF-8') as test_csv:
        first_line = test_csv.readline().rstrip()
        #Test that csv isn't empty
        assert first_line == "ID,Title,Text,Status,Subject"
        #Test that bill was pulled and added to csv by cheking if the bill ID has been written
        test_csv.readline()
        third_line = test_csv.readline()
        csv_row = third_line.split(",")
        bill_id = csv_row[0]
        print(bill_id)
        assert bill_id.isdigit() is True
        #Try to delete the test csv, if permission is denied catch exception
        try:
            os.remove(test_fname)
        except OSError as error:
            print(f"Error: {error.filename} - {error.strerror}.")
