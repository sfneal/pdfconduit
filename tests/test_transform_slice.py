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
    def test_slice_pypdf3_only_first_page(self):
        """Slice a page range from a PDF to create a new 'trimmed' pdf file."""
        fp = 1
        lp = 1
        sliced = slicer(
            self.pdf_path,
            first_page=fp,
            last_page=lp,
            tempdir=self.temp.name,
            method="pypdf3",
        )

        self.assertPdfExists(sliced)
        self.assertCorrectPagesSliced(fp, lp, sliced)

        expected_equals_output(function_name_to_file_name(), sliced)

    @Timer.decorator
    def test_slice_pypdf3_4th_through_7th_pages(self):
        """Slice a page range from a PDF to create a new 'trimmed' pdf file."""
        fp = 4
        lp = 7
        sliced = slicer(
            self.pdf_path,
            first_page=fp,
            last_page=lp,
            tempdir=self.temp.name,
            method="pypdf3",
        )

        self.assertPdfExists(sliced)
        self.assertCorrectPagesSliced(fp, lp, sliced)

        expected_equals_output(function_name_to_file_name(), sliced)

    @Timer.decorator
    def test_slice_pypdf_only_first_page(self):
        """Slice a page range from a PDF to create a new 'trimmed' pdf file."""
        fp = 1
        lp = 1
        sliced = slicer(
            self.pdf_path,
            first_page=fp,
            last_page=lp,
            tempdir=self.temp.name,
            method="pypdf",
        )

        self.assertPdfExists(sliced)
        self.assertCorrectPagesSliced(fp, lp, sliced)

        expected_equals_output(function_name_to_file_name(), sliced)

    @Timer.decorator
    def test_slice_pypdf_4th_through_7th_pages(self):
        """Slice a page range from a PDF to create a new 'trimmed' pdf file."""
        fp = 4
        lp = 7
        sliced = slicer(
            self.pdf_path,
            first_page=fp,
            last_page=lp,
            tempdir=self.temp.name,
            method="pypdf",
        )

        self.assertPdfExists(sliced)
        self.assertCorrectPagesSliced(fp, lp, sliced)

        expected_equals_output(function_name_to_file_name(), sliced)

    def assertCorrectPagesSliced(self, fp, lp, sliced):
        self.assertEqual(Info(sliced).pages, len(range(fp, lp + 1)))

    def assertPdfExists(self, sliced):
        self.assertTrue(os.path.isfile(sliced))


if __name__ == "__main__":
    unittest.main()
