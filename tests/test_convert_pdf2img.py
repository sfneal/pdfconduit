import os
import unittest

from pdfconduit.convert import PDF2IMG
from tests import *


class TestPdf2Img(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdf_path = os.path.join(test_data_dir, "plan_p.pdf")
        cls.img = None

    def tearDown(self):
        if os.path.exists(self.img):
            os.remove(self.img)

    def test_pdf2img(self):
        """Convert a PDF file to a png image."""
        img = PDF2IMG(self.pdf_path).save()

        # Assert img file exists
        self.assertTrue(os.path.exists(img[0]))

        # Assert img file is correct file type
        self.assertTrue(img[0].endswith(".png"))
        self.img = img[0]


if __name__ == "__main__":
    unittest.main()
