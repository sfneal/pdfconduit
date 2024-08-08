from typing import Tuple, List

from parameterized import parameterized

from pdfconduit import Info, Conduit
from tests import test_data_path
from tests.pdfconduit import PdfconduitTestCase


def flatten_params() -> List[str]:
    return list(map(lambda filename: test_data_path(filename), [
        'article.pdf',
        'charts.pdf',
        'document.pdf',
    ]))


def flatten_name_func(testcase_func, param_num, param):
    return "{}_{}".format(testcase_func.__name__, str(param.args[0]))


class TestFlatten(PdfconduitTestCase):
    @parameterized.expand(flatten_params, name_func=flatten_name_func)
    def test_flatten(self, pdf_path: str):
        self.conduit = Conduit(pdf_path).set_output_directory(self.temp.name)
        self.conduit.flatten().write()

        info_og = Info(pdf_path)
        info_flat = Info(self.conduit.output)

        self.assertPdfExists(self.conduit.output)

        # Assert there are the same number of pages in the 'original' and 'flattened' pdf
        self.assertEqual(info_og.pages, info_flat.pages)

        # Confirm that PDF page sizes have not increased
        self.assertTrue(abs(info_og.size[0] / info_flat.size[0]) <= 1)
        self.assertTrue(abs(info_og.size[1] / info_flat.size[1]) <= 1)