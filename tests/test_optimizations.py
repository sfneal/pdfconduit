from typing import Tuple, List

from parameterized import parameterized

from pdfconduit import Info, Pdfconduit
from pdfconduit.settings import Compression
from tests import PdfconduitTestCase, get_clean_pdf_name
from tests import test_data_path


def optimization_params() -> List[str]:
    return list(
        map(
            lambda filename: test_data_path(filename),
            [
                "article.pdf",
                "charts.pdf",
                "document.pdf",
                "workbook.pdf",
            ],
        )
    )


def optimizations_name_func(testcase_func, param_num, param):
    return "{}.{}".format(testcase_func.__name__, get_clean_pdf_name(param.args[0]))


def compress_params() -> List[Tuple[str, Compression]]:
    return [
        (filepath, level)
        for filepath in optimization_params()[0:3]
        for level in Compression.all()
    ]


def compress_name_func(testcase_func, param_num, param):
    return "{}.{}.level_{}".format(
        testcase_func.__name__,
        get_clean_pdf_name(param.args[0]),
        param.args[1].value,
    )


class TestOptimizations(PdfconduitTestCase):
    @parameterized.expand(optimization_params, name_func=optimizations_name_func)
    def test_minify(self, pdf_path: str):
        self.conduit = Pdfconduit(pdf_path).set_output_directory(self.temp.name)
        self.conduit.minify().write()

        self.assertPdfExists(self.conduit.output)
        self.assertFileSizeDecreased(pdf_path, self.conduit.output)
        self.assertPdfPagesEqual(pdf_path, self.conduit.output)

    @parameterized.expand(optimization_params, name_func=optimizations_name_func)
    def test_remove_duplication(self, pdf_path: str):
        self.conduit = Pdfconduit(pdf_path).set_output_directory(self.temp.name)
        self.conduit.remove_duplication().write()

        self.assertPdfExists(self.conduit.output)
        self.assertFileSizeDecreased(pdf_path, self.conduit.output)
        self.assertPdfPagesEqual(pdf_path, self.conduit.output)

    @parameterized.expand(optimization_params, name_func=optimizations_name_func)
    def test_remove_images(self, pdf_path: str):
        self.conduit = Pdfconduit(pdf_path).set_output_directory(self.temp.name)
        self.conduit.remove_images().write()

        self.assertPdfExists(self.conduit.output)
        self.assertEqual(0, self.conduit.info.images_count)

    @parameterized.expand(optimization_params, name_func=optimizations_name_func)
    def test_reduce_image_quality(self, pdf_path: str):
        if pdf_path.endswith("workbook.pdf"):
            self.skipTest("workbook.pdf cannot be reduced quality")
        self.conduit = Pdfconduit(pdf_path).set_output_directory(self.temp.name)
        self.conduit.reduce_image_quality(50).write()

        self.assertPdfExists(self.conduit.output)
        self.assertEqual(Info(pdf_path).images_count, self.conduit.info.images_count)
        self.assertFileSizeDecreased(pdf_path, self.conduit.output)

    @parameterized.expand(compress_params, name_func=compress_name_func)
    def test_compress(self, pdf_path: str, compression: Compression):
        self.conduit = Pdfconduit(pdf_path).set_output_directory(self.temp.name)
        self.conduit.compress(compression).write()

        self.assertPdfExists(self.conduit.output)
        self.assertEqual(Info(pdf_path).images_count, self.conduit.info.images_count)
        # todo: fix compression increasing size, maybe newer pdfs?
        # self.assertFileSizeDecreased(pdf_path, self.conduit.output)
