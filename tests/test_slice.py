import unittest
import os
import shutil
import time
from pdfconduit import Info, slicer
from tests import *


class TestSlice(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Destination directory
        results = os.path.join(directory, 'results')
        if not os.path.isdir(results):
            os.mkdir(results)
        cls.dst = os.path.join(results, 'slice')

        # Create destination if it does not exist
        if not os.path.isdir(cls.dst):
            os.mkdir(cls.dst)

        cls.files = []

        # Log destination
        cls.file_path = 'slice.csv'
        cls.csv = os.path.join(os.path.dirname(__file__), 'log', cls.file_path)
        cls.log = []

    @classmethod
    def tearDownClass(cls):
        write_log(cls.csv, cls.log)

    def setUp(self):
        self.pdf = os.path.join(directory, pdf)
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print("%s: %.3f" % (' '.join(self.id().split('.')[-1].split('_')[1:]), t))

        print(self.defaultTestResult())

        # Log dump
        rows, file_path = dump_log(test_case=self.id().split('.'), time=t)
        self.log.append(rows)
        self.file_path = file_path

        # Move each file into results folder
        for i in self.files:
            source = i
            if os.path.isfile(source):
                target = os.path.join(self.dst, str(os.path.basename(i)))
                try:
                    shutil.move(source, target)
                    self.files.remove(i)
                except FileNotFoundError:
                    pass

    def test_slice(self):
        fp = 1
        lp = 1
        sliced = slicer(self.pdf, first_page=fp, last_page=lp)
        self.files.append(sliced)

        self.assertTrue(os.path.isfile(sliced))
        self.assertEqual(Info(sliced).pages, len(range(fp, lp+1)))

    def test_slice_4to7(self):
        fp = 4
        lp = 7
        sliced = slicer(self.pdf, first_page=fp, last_page=lp, suffix='sliced_4-7')
        self.files.append(sliced)

        self.assertTrue(os.path.isfile(sliced))
        self.assertEqual(Info(sliced).pages, len(range(fp, lp+1)))


if __name__ == '__main__':
    m = unittest.main()
