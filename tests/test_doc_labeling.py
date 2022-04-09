import unittest
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from src.label_documents import log_output_success

class DocumentLabelingTestCase(unittest.TestCase):
    #Tests all elements of the document labeling process

    def test_success_fail(self):
        #Test if the log correctly outputes 'SUCCESS' or 'FAIL'
        success_output = log_output_success(False,'file_name.pdf')
        self.assertEqual(success_output, 'FAIL file_name.pdf')

unittest.main()