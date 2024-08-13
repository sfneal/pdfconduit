import os
import unittest
from tempfile import TemporaryDirectory

from pdfconduit.convert import IMG2PDF
from tests import *


class TestImg2Pdf(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.img_path = img_path
        cls.pdf = None
        cls.tempdir = TemporaryDirectory()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "tempdir"):
            cls.tempdir.cleanup()

    def tearDown(self):
        if os.path.exists(self.pdf):
            os.remove(self.pdf)

    def test_convert(self):
        """Convert an image file into PDF."""
        ip = IMG2PDF(tempdir=self.tempdir)
        self.pdf = ip.convert(self.img_path)

        # Assert pdf file exists
        self.assertTrue(os.path.exists(self.pdf))

    def test_convert_packet(self):
        """Convert an image file into PDF."""
        self.pdf = IMG2PDF(
            [self.img_path, self.img_path, self.img_path],
            destination=test_data_dir,
            tempdir=self.tempdir,
        ).save(clean_temp=False)

        # Assert pdf file exists
        self.assertTrue(os.path.exists(self.pdf))


if __name__ == "__main__":
    unittest.main()
