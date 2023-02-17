""" Copyright (c) 2014 Chris Poliquin cpoliquin@hbs.edu

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

"""
LegiScan numeric codes for bill status and progress.

"""

# current aggregate status of bill
BILL_STATUS = {1: "Introduced",
               2: "Engrossed",
               3: "Enrolled",
               4: "Passed",
               5: "Vetoed",
               6: "Failed/Dead"}

# significant steps in bill progress.
BILL_PROGRESS = {1: "Introduced",
                 2: "Engrossed",
                 3: "Enrolled",
                 4: "Passed",
                 5: "Vetoed",
                 6: "Failed/Dead",
                 7: "Veto Override",
                 8: "Chapter/Act/Statute",
                 9: "Committee Referral",
                10: "Committee Report Pass",
                11: "Committee Report DNP"}
