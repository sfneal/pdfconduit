import unittest
import os
from pdfconduit import Info, rotate
from tests import pdf


class TestRotate(unittest.TestCase):
    def test_rotate(self):
        r = 90
        rotated1 = rotate(pdf, r)

        self.assertTrue(os.path.isfile(rotated1))
        self.assertEqual(Info(rotated1).rotate, r)

    def test_rotate_90(self):
        r = 90
        rotated1 = rotate(pdf, r, suffix='rotated_90')

        self.assertTrue(os.path.isfile(rotated1))
        self.assertEqual(Info(rotated1).rotate, r)

    def test_rotate_180(self):
        r = 180
        rotated1 = rotate(pdf, r, suffix='rotated_180')

        self.assertTrue(os.path.isfile(rotated1))
        self.assertEqual(Info(rotated1).rotate, r)

    def test_rotate_270(self):
        r = 270
        rotated1 = rotate(pdf, r, suffix='rotated_270')

        self.assertTrue(os.path.isfile(rotated1))
        self.assertEqual(Info(rotated1).rotate, r)


if __name__ == '__main__':
    unittest.main()
