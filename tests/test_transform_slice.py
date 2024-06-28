import os
import unittest
from tempfile import TemporaryDirectory

from looptools import Timer

from pdfconduit import Info, slicer
from tests import *


class TestSlice(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdf_path = pdf_path

    def setUp(self):
        self.temp = TemporaryDirectory()

    def tearDown(self):
        self.temp.cleanup()

    @Timer.decorator
    def test_slice_only_first_page(self):
        """Slice a page range from a PDF to create a new 'trimmed' pdf file."""
        fp = 1
        lp = 1
        sliced = slicer(self.pdf_path, first_page=fp, last_page=lp, tempdir=self.temp.name)

        # Assert sliced file exists
        self.assertTrue(os.path.isfile(sliced))

        # Confirm slicer sliced the correct number of pages
        self.assertEqual(Info(sliced).pages, len(range(fp, lp + 1)))

    @Timer.decorator
    def test_slice_4th_through_7th_pages(self):
        """Slice a page range from a PDF to create a new 'trimmed' pdf file."""
        fp = 4
        lp = 7
        sliced = slicer(self.pdf_path, first_page=fp, last_page=lp, tempdir=self.temp.name)

        # Assert sliced file exists
        self.assertTrue(os.path.isfile(sliced))

        # Confirm slicer sliced the correct number of pages
        self.assertEqual(Info(sliced).pages, len(range(fp, lp + 1)))


if __name__ == '__main__':
    unittest.main()
