import unittest
import os
from pdfconduit import Info, Flatten
from tests import *


class TestFlatten(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdf_path = pdf_path

    def test_flatten(self):
        flat = Flatten(self.pdf_path, scale=1.0, suffix='flat_1x').save()

        self.assertTrue(os.path.exists(flat))
        self.assertEqual(Info(self.pdf_path).pages, Info(flat).pages)
        self.assertTrue(abs(Info(self.pdf_path).size[0] / Info(flat).size[0]) <= 1)
        self.assertTrue(abs(Info(self.pdf_path).size[1] / Info(flat).size[1]) <= 1)


if __name__ == '__main__':
    unittest.main()
