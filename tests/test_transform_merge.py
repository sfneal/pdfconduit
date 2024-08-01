import os
import unittest
from tempfile import TemporaryDirectory

from looptools import Timer
from parameterized import parameterized

from pdfconduit import Info, Merge
from pdfconduit.utils.driver import Driver
from tests import *


def merge_params():
    return [
        ('pdfrw', Driver.pdfrw),
        ('pypdf', Driver.pypdf),
    ]


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

    @parameterized.expand(merge_params)
    def test_merge(self, name: str, driver: Driver):
        merger = Merge(self.pdfs, output_name="merged_{}".format(name), output_dir=self.temp.name)
        merger.use(driver).merge()

        # Assert merged file exists
        self.assertTrue(os.path.exists(merger.file))

        # Assert sum of pages in original pdf files equals sum of pages in merged pdf
        self.assertEqual(
            sum([Info(pdf).pages for pdf in self.pdfs]), Info(merger.file).pages
        )

        # Assert metadata was added correctly
        metadata = Info(merger.output).metadata
        if driver == Driver.pdfrw:
            self.assertEqual(metadata["/Producer"], "pdfconduit")
            self.assertEqual(metadata["/Creator"], "pdfconduit")
            self.assertEqual(metadata["/Author"], "Stephen Neal")
        else:
            self.assertEqual(metadata["/Producer"], "pypdf")


if __name__ == "__main__":
    unittest.main()
