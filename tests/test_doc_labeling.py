from unittest import TestCase
import unittest
from label_documents import log_output_success

class DocumentLabelingTestCase(unittest.TestCase):
    #Tests all elements of the document labeling process

    def test_success_fail(self):
        #Test if the log correctly outputes 'SUCCESS' or 'FAIL'
        success_output = log_output_success(True, 'file_name.pdf')
        self.assertEqual(success_output, 'SUCCESS file_name.pdf')

unittest.main()