import os
import unittest
from typing import List

from parameterized import parameterized

from pdfconduit.convert import PDF2IMG
from pdfconduit.convert.pdf2img import ImageExtension
from tests import *


def convert_pdf2img_params() -> List[str]:
    return list(
        map(
            lambda filename: test_data_path(filename),
            [
                "article.pdf",
                "charts.pdf",
                "document.pdf",
                "plan_p.pdf",
            ],
        )
    )


def convert_pdf2img_name_func(testcase_func, param_num, param):
    return "{}.{}".format(testcase_func.__name__, get_clean_pdf_name(param.args[0]))


class TestPdf2Img(PdfconduitTestCase):
    @parameterized.expand(convert_pdf2img_params, name_func=convert_pdf2img_name_func)
    def test_convert_pdf_to_images(self, pdf: str):
        images = PDF2IMG(pdf).convert()

        for image in images:
            # Assert img file exists
            self.assertTrue(os.path.exists(image))

            # Assert img file is correct file type
            self.assertTrue(image.endswith(".png"))

    @parameterized.expand(convert_pdf2img_params, name_func=convert_pdf2img_name_func)
    def test_convert_pdf_to_images_jpg(self, pdf: str):
        images = PDF2IMG(pdf, ext=ImageExtension.JPG).convert()

        for image in images:
            # Assert img file exists
            self.assertTrue(os.path.exists(image))

            # Assert img file is correct file type
            self.assertTrue(image.endswith(".jpg"))

    @parameterized.expand(convert_pdf2img_params, name_func=convert_pdf2img_name_func)
    def test_convert_pdf_to_images_from_stream(self, pdf: str):
        images = PDF2IMG(self._get_pdf_byte_stream(pdf)).convert()

        for image in images:
            # Assert img file exists
            self.assertTrue(os.path.exists(image))

            # Assert img file is correct file type
            self.assertTrue(image.endswith(".png"))

    @parameterized.expand(convert_pdf2img_params, name_func=convert_pdf2img_name_func)
    def test_convert_pdf_to_images_jpg_from_stream(self, pdf: str):
        images = PDF2IMG(
            self._get_pdf_byte_stream(pdf), ext=ImageExtension.JPG
        ).convert()

        for image in images:
            # Assert img file exists
            self.assertTrue(os.path.exists(image))

            # Assert img file is correct file type
            self.assertTrue(image.endswith(".jpg"))


if __name__ == "__main__":
    unittest.main()
