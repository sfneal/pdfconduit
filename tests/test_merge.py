import os.path
from typing import Iterable

from parameterized import parameterized

from pdfconduit import Conduit, Info
from tests import PdfconduitTestCase
from tests import test_data_path


def merge_params():
    params = [
        ("document.pdf", ["article.pdf", "manual.pdf"]),
        ("document.pdf", ["workbook.pdf", "article.pdf"]),
        ("workbook.pdf", ["document.pdf", "article.pdf"]),
        ("article.pdf", ["document.pdf"]),
        ("document.pdf", ["workbook.pdf", "document.pdf"]),
    ]
    return [
        (test_data_path(main_pdf), list(map(lambda pdf: test_data_path(pdf), to_merge)))
        for main_pdf, to_merge in params
    ]


def merge_name_func(testcase_func, param_num, param):
    return "{}_{}_{}_{}".format(
        testcase_func.__name__,
        param_num,
        os.path.basename(param.args[0]),
        len(param.args[1]),
    )


class TestMerge(PdfconduitTestCase):
    @parameterized.expand(merge_params, name_func=merge_name_func)
    def test_can_merge_pdfs(self, main_pdf: str, pdfs_to_merge: Iterable[str]):
        self.pdf_path = main_pdf
        self.conduit = Conduit(main_pdf).set_output_directory(self.temp.name)

        for pdf in pdfs_to_merge:
            self.conduit.merge(pdf)

        self.conduit.write()

        self.assertPdfExists(self.conduit.output)
        self.assertCorrectNumPages(main_pdf, pdfs_to_merge, self.conduit.info.pages)

    @parameterized.expand(merge_params, name_func=merge_name_func)
    def test_can_merge_pdfs_using_context(
        self, main_pdf: str, pdfs_to_merge: Iterable[str]
    ):
        self.pdf_path = main_pdf
        with Conduit(self.pdf_path) as conduit:
            conduit.set_output_directory(self.temp.name)
            for pdf in pdfs_to_merge:
                conduit.merge(pdf)

        self.assertPdfExists(conduit.output)
        self.assertCorrectNumPages(main_pdf, pdfs_to_merge, conduit.info.pages)

    @parameterized.expand(merge_params, name_func=merge_name_func)
    def test_can_merge_pdfs_fast(self, main_pdf: str, pdfs_to_merge: list[str]):
        self.pdf_path = main_pdf
        self.conduit = Conduit(main_pdf).set_output_directory(self.temp.name)

        self.conduit.merge_fast(pdfs_to_merge)

        self.conduit.write()

        self.assertPdfExists(self.conduit.output)
        self.assertCorrectNumPages(main_pdf, pdfs_to_merge, self.conduit.info.pages)

    def assertPdfExists(self, path: str) -> None:
        self.assertTrue(os.path.exists(path))

    def assertCorrectNumPages(
        self, main_pdf: str, pdfs_to_merge: Iterable[str], expected_pages: int
    ) -> None:
        # Assert sum of pages in original pdf files equals sum of pages in merged pdf
        self.assertEqual(
            sum([Info(pdf).pages for pdf in pdfs_to_merge]) + Info(main_pdf).pages,
            expected_pages,
        )
