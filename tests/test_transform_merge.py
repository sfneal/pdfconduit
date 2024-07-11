import os
import unittest
from tempfile import TemporaryDirectory

from looptools import Timer

from pdfconduit import Info, Merge
from tests import *


class TestMerge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdfs = [
            os.path.join(test_data_dir, p)
            for p in ["article.pdf", "charts.pdf", "document.pdf", "manual.pdf"]
        ]

    def setUp(self):
        self.temp = TemporaryDirectory()

    def tearDown(self):
        self.temp.cleanup()

    @Timer.decorator
    def test_merge_pdfrw(self):
        """Merge multiple PDF files into a single PDF using the `pdfrw` library."""
        merged = Merge(
            self.pdfs,
            output_name="merged_pdfrw",
            output_dir=self.temp.name,
            method="pdfrw",
        )
        merged.merge()

        # Assert merged file exists
        self.assertTrue(os.path.exists(merged.file))

        # Assert sum of pages in original pdf files equals sum of pages in merged pdf
        self.assertEqual(
            sum([Info(pdf).pages for pdf in self.pdfs]), Info(merged.file).pages
        )

        # Assert metadata was added correctly
        metadata = Info(merged.output).metadata
        self.assertEqual(metadata["/Producer"], "pdfconduit")
        self.assertEqual(metadata["/Creator"], "pdfconduit")
        self.assertEqual(metadata["/Author"], "Stephen Neal")

        expected_equals_output(function_name_to_file_name(), merged.output)

    @Timer.decorator
    def test_merge_pypdf(self):
        """Merge multiple PDF files into a single PDF using the `pypdf` library."""
        merged = Merge(
            self.pdfs,
            output_name="merged_pypdf",
            output_dir=self.temp.name,
            method="pypdf",
        )
        merged.merge()

        # Assert merged file exists
        self.assertTrue(os.path.exists(merged.file))

        # Assert sum of pages in original pdf files equals sum of pages in merged pdf
        self.assertEqual(
            sum([Info(pdf).pages for pdf in self.pdfs]), Info(merged.file).pages
        )

        # Assert metadata was added correctly
        metadata = Info(merged.output).metadata
        self.assertEqual(metadata["/Producer"], "pypdf")

        expected_equals_output(function_name_to_file_name(), merged.output)


if __name__ == "__main__":
    unittest.main()
