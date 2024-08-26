from typing import List

from parameterized import parameterized

from pdfconduit import Pdfconduit
from tests import PdfconduitTestCase, get_clean_pdf_name
from tests import test_data_path


def flatten_params() -> List[str]:
    return list(
        map(
            lambda filename: test_data_path(filename),
            [
                "article.pdf",
                "charts.pdf",
                "document.pdf",
            ],
        )
    )


def flatten_name_func(testcase_func, param_num, param):
    return "{}.{}".format(testcase_func.__name__, get_clean_pdf_name(param.args[0]))


class TestFlatten(PdfconduitTestCase):
    @parameterized.expand(flatten_params, name_func=flatten_name_func)
    def test_flatten(self, pdf_path: str):
        self.conduit = Pdfconduit(pdf_path).set_output_directory(self.temp.name)
        self.conduit.flatten().write()

        self.assertPdfExists(self.conduit.output)
        self.assertPdfPagesEqual(pdf_path, self.conduit.output)
        # todo: improve assertions

    @parameterized.expand(flatten_params, name_func=flatten_name_func)
    def test_flatten_from_stram(self, pdf_path: str):
        self.conduit = Pdfconduit(
            self._get_pdf_byte_stream(pdf_path)
        ).set_output_directory(self.temp.name)
        self.conduit.flatten().write()

        self.assertPdfExists(self.conduit.output)
        self.assertPdfPagesEqual(pdf_path, self.conduit.output)
        # todo: improve assertions
