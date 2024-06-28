import os
import unittest

from looptools import Timer

from pdfconduit import Info, Flatten
from tests import *


class TestFlatten(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdf_path = pdf_path
        cls.flat = None

    def tearDown(self):
        if os.path.exists(self.flat):
            os.remove(self.flat)

    @Timer.decorator
    def test_flatten(self):
        """Create a 'flattened' pdf file without layers."""
        self.flat = Flatten(self.pdf_path, suffix='flat').save()

        info_og = Info(self.pdf_path)
        info_flat = Info(self.flat)

        # Assert pdf file exists
        self.assertTrue(os.path.exists(self.flat))

        # Assert there are the same number of pages in the 'original' and 'flattened' pdf
        self.assertEqual(info_og.pages, info_flat.pages)

        # Confirm that PDF page sizes have not increased
        self.assertTrue(abs(info_og.size[0] / info_flat.size[0]) <= 1)
        self.assertTrue(abs(info_og.size[1] / info_flat.size[1]) <= 1)


if __name__ == '__main__':
    unittest.main()
