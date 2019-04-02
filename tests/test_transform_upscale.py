import os
import unittest
from tempfile import TemporaryDirectory

from looptools import Timer

from pdfconduit import Info, upscale
from tests import *


class TestTransformUpscale(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdf_path = pdf_path

    def setUp(self):
        self.temp = TemporaryDirectory()

    def tearDown(self):
        self.temp.cleanup()

    @Timer.decorator
    def test_upscale_pdfrw_20x(self):
        """Resize a PDF file to 2.0x times the original scale."""
        s = 2.0
        upscaled = upscale(pdf_path, scale=s, suffix='upscaled_2.0_pdfrw', tempdir=self.temp.name, method='pdfrw')

        # Assert upscaled file exists
        self.assertTrue(os.path.isfile(upscaled))

        # Assert upscaled pdf file is the correct size
        self.assertEqual(Info(upscaled).size, tuple([i * s for i in Info(pdf_path).size]))
        return upscaled

    @Timer.decorator
    def test_upscale_pdfrw_15x(self):
        """Resize a PDF file to 1.5x times the original scale."""
        s = 1.5
        upscaled = upscale(pdf_path, scale=s, suffix='upscaled_1.5_pdfrw', tempdir=self.temp.name, method='pdfrw')

        # Assert upscaled file exists
        self.assertTrue(os.path.isfile(upscaled))

        # Assert upscaled pdf file is the correct size
        self.assertEqual(Info(upscaled).size, tuple([i * s for i in Info(pdf_path).size]))
        return upscaled

    @Timer.decorator
    def test_upscale_pdfrw_30x(self):
        """Resize a PDF file to 3.0x times the original scale."""
        s = 3.0
        upscaled = upscale(pdf_path, scale=s, suffix='upscaled_3.0_pdfrw', tempdir=self.temp.name, method='pdfrw')

        # Assert upscaled file exists
        self.assertTrue(os.path.isfile(upscaled))

        # Assert upscaled pdf file is the correct size
        self.assertEqual(Info(upscaled).size, tuple([i * s for i in Info(pdf_path).size]))
        return upscaled


if __name__ == '__main__':
    unittest.main()
