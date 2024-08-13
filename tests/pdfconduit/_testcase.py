import json
import os
import unittest
from decimal import Decimal
from tempfile import TemporaryDirectory
from time import time

from pdfconduit import Conduit, Info
from tests import pdf_path, get_output_filepath


class PdfconduitTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Encryption passwords
        cls.owner_pw = "foo"
        cls.user_pw = "baz"
        cls.pdf_path = pdf_path
        cls.timings = {}

    def setUp(self):
        self.temp = TemporaryDirectory()
        self.conduit = Conduit(self.pdf_path).set_output_directory(self.temp.name)
        self.timer = Timer()

    def tearDown(self):
        self.temp.cleanup()
        self.timings[self.id()] = self.timer.end

    @classmethod
    def tearDownClass(cls):
        json_path = get_output_filepath('timings.json')

        if os.path.isfile(json_path):
            with open(json_path, 'r') as json_file:
                data = json.load(json_file)

            data.update(cls.timings)
        else:
            data = cls.timings

        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=2, sort_keys=True)

    def assertPdfExists(self, pdf):
        self.assertTrue(os.path.exists(pdf))
        self.assertTrue(os.path.isfile(pdf))

    def assertPdfDoesntExists(self, pdf):
        self.assertFalse(os.path.exists(pdf))
        self.assertFalse(os.path.isfile(pdf))

    def assertPdfPagesEqual(self, original: str, modified: str):
        info_og = Info(original)
        info_modified = Info(modified)
        self.assertEqual(info_og.pages, info_modified.pages)
        self.assertTrue(abs(info_og.size[0] / info_modified.size[0]) <= 1)
        self.assertTrue(abs(info_og.size[1] / info_modified.size[1]) <= 1)


class Timer:
    def __init__(self, decimal_places=2):
        self._decimal_places = decimal_places

        self.start = time()

    @property
    def end(self):
        # Calculate run time
        return self.human_time(time() - self.start)

    @staticmethod
    def rounder(exact, decimals=2):
        """Round a float to a certain number of decimal places."""
        return float(round(Decimal(exact), decimals))

    def human_time(self, runtime):
        """Display runtime in a human friendly format."""
        return self.rounder(runtime * 1000, self._decimal_places)