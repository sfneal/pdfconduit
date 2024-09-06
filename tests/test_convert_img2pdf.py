import os
import unittest
from tempfile import NamedTemporaryFile, TemporaryDirectory

from pdfconduit import Info
from pdfconduit.convert import IMG2PDF
from tests import *


class TestImg2Pdf(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.img_path = img_path
        cls.pdf = None

    def setUp(self):
        self.tempdir = TemporaryDirectory()

    def tearDown(self):
        self.tempdir.cleanup()

    def test_convert(self):
        with NamedTemporaryFile(suffix=".pdf", dir=self.tempdir.name) as tempfile:
            ip = IMG2PDF(self.img_path, output=tempfile.name, tempdir=self.tempdir)
            self.pdf = ip.convert()

            # Assert pdf file exists
            self.assertTrue(os.path.exists(self.pdf))
            self.assertEqual(1, Info(self.pdf).pages)
        ip.cleanup()

    def test_convert_packet(self):
        with NamedTemporaryFile(suffix=".pdf", dir=self.tempdir.name) as tempfile:
            ip = IMG2PDF(
                [self.img_path, self.img_path, self.img_path],
                output=tempfile.name,
                tempdir=self.tempdir,
            )
            self.pdf = ip.convert()

            # Assert pdf file exists
            self.assertTrue(os.path.exists(self.pdf))
            self.assertEqual(3, Info(self.pdf).pages)
        ip.cleanup()


if __name__ == "__main__":
    unittest.main()
