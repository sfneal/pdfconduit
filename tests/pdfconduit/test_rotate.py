import unittest
import os
import shutil
from pdfconduit import Info, rotate
from tests import pdf, directory


class TestRotate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = []

    @classmethod
    def tearDownClass(cls):
        # Destination directory
        dst = os.path.join(directory, 'results', 'rotate')

        # Create destination if it does not exist
        if not os.path.isdir(dst):
            os.mkdir(dst)

        # Move each file into results folder
        for i in cls.files:
            source = i
            target = os.path.join(dst, str(os.path.basename(i)))
            shutil.move(source, target)

    def test_rotate(self):
        r = 90
        rotated1 = rotate(pdf, r)
        self.files.append(rotated1)

        self.assertTrue(os.path.isfile(rotated1))
        self.assertEqual(Info(rotated1).rotate, r)

    def test_rotate_90(self):
        r = 90
        rotated1 = rotate(pdf, r, suffix='rotated_90')
        self.files.append(rotated1)

        self.assertTrue(os.path.isfile(rotated1))
        self.assertEqual(Info(rotated1).rotate, r)

    def test_rotate_180(self):
        r = 180
        rotated1 = rotate(pdf, r, suffix='rotated_180')
        self.files.append(rotated1)

        self.assertTrue(os.path.isfile(rotated1))
        self.assertEqual(Info(rotated1).rotate, r)

    def test_rotate_270(self):
        r = 270
        rotated1 = rotate(pdf, r, suffix='rotated_270')
        self.files.append(rotated1)

        self.assertTrue(os.path.isfile(rotated1))
        self.assertEqual(Info(rotated1).rotate, r)


if __name__ == '__main__':
    unittest.main()
