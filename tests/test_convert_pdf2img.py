import os
import unittest
from typing import List, Tuple

from parameterized import parameterized

from pdfconduit import Pdfconduit
from pdfconduit.convert import PDF2IMG
from pdfconduit.convert.pdf2img import ImageExtension
from tests import *


def params() -> List[Tuple[str, ImageExtension, bool]]:
    files = [
        "article.pdf",
        "charts.pdf",
        "document.pdf",
        "plan_p.pdf",
    ]
    extensions = [ImageExtension.PNG, ImageExtension.JPG]
    from_stream = [True, False]

    return [
        (test_data_path(file), extension, use_stream)
        for use_stream in from_stream
        for extension in extensions
        for file in files
    ]


def name_func(testcase_func, param_num, param):
    return "{}.{}.{}.{}".format(
        testcase_func.__name__,  # test func
        param.args[1].value,  # image extension
        "from_stream" if param.args[2] is True else "from_file",  # stream vs. file
        get_clean_pdf_name(param.args[0]),  # filename
    )


class TestPdf2Img(PdfconduitTestCase):
    @parameterized.expand(params, name_func=name_func)
    def test_convert_pdf_to_images_pdf2img(
        self, pdf: str, ext: ImageExtension, from_stream: bool
    ):
        images = PDF2IMG(
            pdf if not from_stream else self._get_pdf_byte_stream(pdf), ext=ext
        ).convert()

        for image in images:
            # Assert img file exists
            self.assertTrue(os.path.exists(image))

            # Assert img file is correct file type
            self.assertTrue(image.endswith(ext.value))

    @parameterized.expand(params, name_func=name_func)
    def test_convert_pdf_to_images_pdfconduit(
        self, pdf: str, ext: ImageExtension, from_stream: bool
    ):
        images = Pdfconduit(
            pdf if not from_stream else self._get_pdf_byte_stream(pdf)
        ).to_images(ext=ext)

        for image in images:
            # Assert img file exists
            self.assertTrue(os.path.exists(image))

            # Assert img file is correct file type
            self.assertTrue(image.endswith(ext.value))


if __name__ == "__main__":
    unittest.main()
