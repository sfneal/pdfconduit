import unittest
import os
import shutil
import time
from pdf.conduit import Info, Flatten
from tests import *


class TestFlatten(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Destination directory
        results = os.path.join(directory, 'results')
        if not os.path.isdir(results):
            os.mkdir(results)
        cls.dst = os.path.join(results, 'flatten')

        # Create destination if it does not exist
        if not os.path.isdir(cls.dst):
            os.mkdir(cls.dst)

        # Log destination
        cls.file_path = 'flatten.csv'
        cls.csv = os.path.join(os.path.dirname(__file__), 'log', cls.file_path)
        cls.log = []

        cls.fname = pdf

        cls.files = []

    @classmethod
    def tearDownClass(cls):
        write_log(cls.csv, cls.log)

    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = round(time.time() - self.startTime, 2)
        print("{0:15} --> {1}".format(' '.join(self.id().split('.')), t))

        # Log dump
        rows, file_path = dump_log(test_case=self.id().split('.'), time=t)
        self.log.append(rows)
        self.file_path = file_path

        # Move each file into results folder
        for i in self.files:
            source = i
            target = os.path.join(self.dst, str(os.path.basename(i)))
            shutil.move(source, target)
            self.files.remove(i)

    def test_flatten_1x(self):
        flat = Flatten(self.fname, scale=1.0, suffix='flat_1x').save()
        self.files.append(flat)

        self.assertTrue(os.path.exists(flat))
        self.assertEqual(Info(self.fname).pages, Info(flat).pages)
        self.assertTrue(abs(Info(self.fname).size[0] / Info(flat).size[0]) <= 1)
        self.assertTrue(abs(Info(self.fname).size[1] / Info(flat).size[1]) <= 1)

    def test_flatten_2x(self):
        scale = 2.0
        flat = Flatten(self.fname, scale=scale, suffix='flat_2x').save()
        self.files.append(flat)

        self.assertTrue(os.path.exists(flat))
        self.assertEqual(Info(self.fname).pages, Info(flat).pages)
        self.assertTrue(abs(Info(self.fname).size[0] * scale / Info(flat).size[0]) <= 1)
        self.assertTrue(abs(Info(self.fname).size[1] * scale / Info(flat).size[1]) <= 1)

    def test_flatten_3x(self):
        scale = 3.0
        flat = Flatten(self.fname, scale=scale, suffix='flat_3x').save()
        self.files.append(flat)

        self.assertTrue(os.path.exists(flat))
        self.assertEqual(Info(self.fname).pages, Info(flat).pages)
        self.assertTrue(abs(Info(self.fname).size[0] * scale / Info(flat).size[0]) <= 1)
        self.assertTrue(abs(Info(self.fname).size[1] * scale / Info(flat).size[1]) <= 1)


if __name__ == '__main__':
    unittest.main()
