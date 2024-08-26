import inspect
import json
import os
import shutil
import unittest
from decimal import Decimal
from io import BytesIO
from tempfile import TemporaryDirectory
from time import time
from typing import Optional

from pdfconduit import Pdfconduit, Info
from pdfconduit.utils.typing import Iterable

test_data_dir = os.path.join(os.path.dirname(__file__), "data")
# pdf_name = 'plan_l.pdf'
# pdf_name = 'plan_p.pdf'
# pdf_name = 'article.pdf'
pdf_name = "document.pdf"
# pdf_name = 'con docs2.pdf'
img_name = "floor plan.png"
pdf_path = os.path.join(test_data_dir, pdf_name)
img_path = os.path.join(test_data_dir, img_name)


def test_data_path(filename):
    return os.path.join(test_data_dir, filename)


def files_are_equal(file1_path, file2_path):
    """
    Compare two files to check if they are the same.

    Parameters:
    file1_path (str): The path to the first file.
    file2_path (str): The path to the second file.

    Returns:
    bool: True if the files are the same, False otherwise.
    """
    with open(file1_path, "rb") as file1, open(file2_path, "rb") as file2:
        file1_content = file1.read()
        file2_content = file2.read()

    return file1_content == file2_content


def function_name_to_file_name(extension=".pdf"):
    return inspect.stack()[1][3] + extension


def copy_pdf_to_output_directory(pdf, save_name):
    shutil.copy(pdf, get_output_filepath(save_name))


def get_output_filepath(filename):
    return os.path.join(os.path.join(os.path.dirname(__file__), "output"), filename)


def expected_equals_output(test_function, output_filepath):
    return files_are_equal(get_output_filepath(test_function), output_filepath)


def get_clean_pdf_name(path) -> str:
    return os.path.basename(str(path)).replace(".", ",")


# Example usage
# Save outputs to tests/output directory
# copy_pdf_to_output_directory({pdfoutput}, function_name_to_file_name())

# Compare saved outputs to generate pdfs
# expected_equals_output(function_name_to_file_name(), {pdfouput})


class PdfconduitTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Encryption passwords
        cls.owner_pw = "foo"
        cls.user_pw = "baz"
        cls.pdf_path = pdf_path
        cls.timings = {}

    def setUp(self):
        self.temp = TemporaryDirectory()
        self.conduit = Pdfconduit(self.pdf_path).set_output_directory(self.temp.name)
        self.timer = Timer()

    def tearDown(self):
        self.temp.cleanup()
        self.timings[self.id()] = self.timer.end

    @classmethod
    def tearDownClass(cls):
        json_path = test_data_path("timings.json")

        if os.path.isfile(json_path):
            with open(json_path, "r") as json_file:
                data = json.load(json_file)

            data.update(cls.timings)
        else:
            data = cls.timings

        with open(json_path, "w") as json_file:
            json.dump(data, json_file, indent=2, sort_keys=True)

    def assertPdfExists(self, pdf):
        self.assertTrue(os.path.exists(pdf))
        self.assertTrue(os.path.isfile(pdf))

    def assertPdfDoesntExists(self, pdf):
        self.assertFalse(os.path.exists(pdf))
        self.assertFalse(os.path.isfile(pdf))

    def assertPdfPagesEqual(self, original: str, modified: str):
        info_og = Info(original)
        info_modified = Info(modified)
        self.assertEqual(info_og.pages, info_modified.pages)
        self.assertTrue(abs(info_og.size[0] / info_modified.size[0]) <= 1)
        self.assertTrue(abs(info_og.size[1] / info_modified.size[1]) <= 1)

    def assertCorrectNumPages(
        self, main_pdf: str, pdfs_to_merge: Iterable[str], expected_pages: int
    ) -> None:
        # Assert sum of pages in original pdf files equals sum of pages in merged pdf
        self.assertEqual(
            sum([Info(pdf).pages for pdf in pdfs_to_merge]) + Info(main_pdf).pages,
            expected_pages,
        )

    def assertPdfRotation(self, rotated, rotation):
        info = rotated.info if isinstance(rotated, Pdfconduit) else rotated
        self.assertEqual(info.rotate, rotation)

    def assertCorrectPagesSliced(self, fp, lp, sliced):
        info = sliced.info if isinstance(sliced, Pdfconduit) else sliced
        self.assertEqual(info.pages, len(range(fp, lp + 1)))

    def assertPdfScaled(self, scale, scaled, original=None):
        original = self.pdf_path if original is None else original
        info = scaled.info if isinstance(scaled, Pdfconduit) else scaled
        self.assertEqual(info.size, tuple([i * scale for i in Info(original).size]))
        # self.assertEqual(info.pages, Info(original).pages)

    def assertFileSizeDecreased(self, original: str, modified: str):
        self.assertLess(os.path.getsize(modified), os.path.getsize(original))

    def _get_pdf_byte_stream(self, path: Optional[str] = None) -> BytesIO:
        with open(path if path else self.pdf_path, "rb") as fh:
            return BytesIO(fh.read())


class Timer:
    def __init__(self, decimal_places=2):
        self._decimal_places = decimal_places

        self.start = time()

    @property
    def end(self):
        # Calculate run time
        return self.human_time(time() - self.start)

    @staticmethod
    def rounder(exact, decimals=2):
        """Round a float to a certain number of decimal places."""
        return float(round(Decimal(exact), decimals))

    def human_time(self, runtime):
        """Display runtime in a human friendly format."""
        return self.rounder(runtime * 1000, self._decimal_places)


__all__ = [
    "pdf_path",
    "img_path",
    "test_data_dir",
    "test_data_path",
    "function_name_to_file_name",
    "copy_pdf_to_output_directory",
    "expected_equals_output",
    "get_output_filepath",
    "PdfconduitTestCase",
    "get_clean_pdf_name",
]
