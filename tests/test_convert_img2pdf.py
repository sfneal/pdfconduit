import os
import unittest
from tempfile import TemporaryDirectory

from looptools import Timer

from pdf.convert import IMG2PDF
from tests import *


class TestConvertImg2Pdf(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.img_path = img_path
        cls.pdf = None

    def setUp(self):
        self.temp = TemporaryDirectory()

    def tearDown(self):
        self.temp.cleanup()
        if os.path.exists(self.pdf):
            os.remove(self.pdf)

    @Timer.decorator
    def test_convert_img2pdf(self):
        """Convert an image file into PDF."""
        pdf = IMG2PDF([self.img_path], destination=test_data_dir).save(remove_temps=False)

        # Assert pdf file exists
        self.assertTrue(os.path.exists(pdf))
        self.pdf = pdf
        return pdf


if __name__ == '__main__':
    unittest.main()
