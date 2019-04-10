import os
import unittest

from looptools import Timer

from pdf.convert import IMG2PDF
from tests import *


class TestConvertImg2Pdf(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.img_path = img_path
        cls.pdf = None

    def tearDown(self):
        if os.path.exists(self.pdf):
            os.remove(self.pdf)

    @Timer.decorator
    def test_convert(self):
        """Convert an image file into PDF."""
        ip = IMG2PDF()
        self.pdf = ip.convert(self.img_path)
        ip.cleanup()

        # Assert pdf file exists
        self.assertTrue(os.path.exists(self.pdf))
        return self.pdf

    @Timer.decorator
    def test_convert_packet(self):
        """Convert an image file into PDF."""
        self.pdf = IMG2PDF([self.img_path, self.img_path, self.img_path], destination=test_data_dir).save()

        # Assert pdf file exists
        self.assertTrue(os.path.exists(self.pdf))
        return self.pdf


if __name__ == '__main__':
    unittest.main()
