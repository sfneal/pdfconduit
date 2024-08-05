import os
import unittest
from tempfile import TemporaryDirectory
from typing import List

from parameterized import parameterized

from pdfconduit import Info, slicer
from tests import *


def slice_params() -> List[str]:
    return [
        "1to1",
        "4to7",
        "2to6",
        "1to8",
        "4to9",
    ]


class TestSlice(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdf_path = pdf_path

    def setUp(self):
        self.temp = TemporaryDirectory()

    def tearDown(self):
        self.temp.cleanup()

    @parameterized.expand(slice_params)
    def test_slice(self, slice_range: str):
        fp, lp = tuple(slice_range.split("to"))
        fp = int(fp)
        lp = int(lp)

        sliced = slicer(
            self.pdf_path,
            first_page=fp,
            last_page=lp,
            tempdir=self.temp.name,
        )

        self.assertPdfExists(sliced)
        self.assertCorrectPagesSliced(fp, lp, sliced)

    def assertCorrectPagesSliced(self, fp, lp, sliced):
        self.assertEqual(Info(sliced).pages, len(range(fp, lp + 1)))

    def assertPdfExists(self, sliced):
        self.assertTrue(os.path.isfile(sliced))


if __name__ == "__main__":
    unittest.main()
