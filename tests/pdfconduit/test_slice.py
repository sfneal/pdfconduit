import unittest
import os
from pdfconduit import Info, slicer
from tests import directory


class TestSlice(unittest.TestCase):
    def setUp(self):
        self.pdf = os.path.join(directory, 'manual.pdf')

    def test_slice(self):
        fp = 10
        lp = 31
        sliced = slicer(self.pdf, first_page=fp, last_page=lp)

        self.assertTrue(os.path.isfile(sliced))
        self.assertEqual(Info(sliced).pages, len(range(fp, lp+1)))

    def test_slice_15to50(self):
        fp = 15
        lp = 50
        sliced = slicer(self.pdf, first_page=fp, last_page=lp, suffix='sliced_15-50')

        self.assertTrue(os.path.isfile(sliced))
        self.assertEqual(Info(sliced).pages, len(range(fp, lp+1)))


if __name__ == '__main__':
    unittest.main()
