import os
import unittest
from tempfile import TemporaryDirectory

from looptools import Timer

from pdfconduit.convert import IMG2PDF, PDF2IMG
from pdfconduit import Info, Flatten
from tests import *


class TestConvertFlatten(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdf_path = pdf_path
        cls.flat = None

    def tearDown(self):
        if os.path.exists(self.flat):
            os.remove(self.flat)

    @Timer.decorator
    def test_flatten(self):
        """Create a 'flattened' pdf file without layers."""
        flat = Flatten(self.pdf_path, suffix='flat').save()

        # Assert pdf file exists
        self.assertTrue(os.path.exists(flat))

        # Assert there are the same number of pages in the 'original' and 'flattened' pdf
        self.assertEqual(Info(self.pdf_path).pages, Info(flat).pages)

        # Confirm that PDF page sizes have not increased
        self.assertTrue(abs(Info(self.pdf_path).size[0] / Info(flat).size[0]) <= 1)
        self.assertTrue(abs(Info(self.pdf_path).size[1] / Info(flat).size[1]) <= 1)
        self.flat = flat
        return flat


class TestConvertImg2Pdf(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.img_path = img_path
        cls.pdf = None
        cls.tempdir = TemporaryDirectory()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'tempdir'):
            cls.tempdir.cleanup()

    def tearDown(self):
        if os.path.exists(self.pdf):
            os.remove(self.pdf)

    @Timer.decorator
    def test_convert(self):
        """Convert an image file into PDF."""
        ip = IMG2PDF(tempdir=self.tempdir)
        self.pdf = ip.convert(self.img_path)

        # Assert pdf file exists
        self.assertTrue(os.path.exists(self.pdf))
        return self.pdf

    @Timer.decorator
    def test_convert_packet(self):
        """Convert an image file into PDF."""
        self.pdf = IMG2PDF([self.img_path, self.img_path, self.img_path],
                           destination=test_data_dir,
                           tempdir=self.tempdir).save(clean_temp=False)

        # Assert pdf file exists
        self.assertTrue(os.path.exists(self.pdf))
        return self.pdf


class TestConvertPdf2Img(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdf_path = os.path.join(test_data_dir, 'plan_p.pdf')
        cls.img = None

    def tearDown(self):
        if os.path.exists(self.img):
            os.remove(self.img)

    @Timer.decorator
    def test_pdf2img(self):
        """Convert a PDF file to a png image."""
        img = PDF2IMG(self.pdf_path).save()

        # Assert img file exists
        self.assertTrue(os.path.exists(img[0]))

        # Assert img file is correct file type
        self.assertTrue(img[0].endswith('.png'))
        self.img = img[0]
        return img[0]


if __name__ == '__main__':
    unittest.main()
