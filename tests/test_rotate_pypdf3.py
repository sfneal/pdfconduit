import unittest
import os
import shutil
import time
from pdfconduit import Info, rotate
from tests import *


class TestRotatePyPDF3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Destination directory
        results = os.path.join(directory, 'results')
        if not os.path.isdir(results):
            os.mkdir(results)
        cls.dst = os.path.join(results, 'rotate')

        # Create destination if it does not exist
        if not os.path.isdir(cls.dst):
            os.mkdir(cls.dst)

        # Log destination
        cls.file_path = 'rotate_pypdf3.csv'
        cls.csv = os.path.join(os.path.dirname(__file__), 'log', cls.file_path)
        cls.log = []

        cls.files = []

    @classmethod
    def tearDownClass(cls):
        write_log(cls.csv, cls.log)

    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print("{0:15} --> {1}".format(' '.join(self.id().split('.')[-1].split('_')[2:]), t))

        # Log dump
        rows, file_path = dump_log(test_case=self.id().split('.'), time=t)
        self.log.append(rows)
        self.file_path = file_path

        # Move each file into results folder
        for i in self.files:
            source = i
            target = os.path.join(self.dst, str(os.path.basename(i)))
            try:
                shutil.move(source, target)
                self.files.remove(i)
            except FileNotFoundError:
                pass

    def test_rotate_pypdf3(self):
        r = 90
        rotated1 = rotate(pdf, r, suffix='rotated_pypdf3', method='pypdf3')
        self.files.append(rotated1)

        self.assertTrue(os.path.isfile(rotated1))
        self.assertEqual(Info(rotated1).rotate, r)

    def test_rotate_90_pypdf3(self):
        r = 90
        rotated1 = rotate(pdf, r, suffix='rotated_90_pypdf3', method='pypdf3')
        self.files.append(rotated1)

        self.assertTrue(os.path.isfile(rotated1))
        self.assertEqual(Info(rotated1).rotate, r)

    def test_rotate_180_pypdf3(self):
        r = 180
        rotated1 = rotate(pdf, r, suffix='rotated_180_pypdf3', method='pypdf3')
        self.files.append(rotated1)

        self.assertTrue(os.path.isfile(rotated1))
        self.assertEqual(Info(rotated1).rotate, r)

    def test_rotate_270_pypdf3(self):
        r = 270
        rotated1 = rotate(pdf, r, suffix='rotated_270_pypdf3', method='pypdf3')
        self.files.append(rotated1)

        self.assertTrue(os.path.isfile(rotated1))
        self.assertEqual(Info(rotated1).rotate, r)


if __name__ == '__main__':
    unittest.main()
