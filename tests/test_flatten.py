import os.path
from typing import List

from parameterized import parameterized

from pdfconduit import Conduit
from tests import PdfconduitTestCase
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
    return "{}_{}".format(testcase_func.__name__, os.path.basename(str(param.args[0])))


class TestFlatten(PdfconduitTestCase):
    @parameterized.expand(flatten_params, name_func=flatten_name_func)
    def test_flatten(self, pdf_path: str):
        self.conduit = Conduit(pdf_path).set_output_directory(self.temp.name)
        self.conduit.flatten().write()

        self.assertPdfExists(self.conduit.output)
        self.assertPdfPagesEqual(pdf_path, self.conduit.output)
