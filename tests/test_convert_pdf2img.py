import unittest
import os
from tempfile import TemporaryDirectory
from looptools import Timer
from pdf.convert import PDF2IMG
from tests import *


class TestConvertPdf2Img(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdf_path = os.path.join(test_data_dir, 'plan_p.pdf')
        cls.img = None

    def setUp(self):
        self.temp = TemporaryDirectory()

    def tearDown(self):
        self.temp.cleanup()
        if os.path.exists(self.img):
            os.remove(self.img)

    @Timer.decorator
    def test_convert_pdf2img(self):
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
