import os
import unittest
from tempfile import TemporaryDirectory

from looptools import Timer

from pdfconduit import Info, Rotate
from tests import *


class TestRotate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdf_path = pdf_path

    def setUp(self):
        self.temp = TemporaryDirectory()

    def tearDown(self):
        self.temp.cleanup()

    @Timer.decorator
    def test_rotate_pdfrw_90(self):
        """Rotate a PDF file by 90 degrees using the `pdfrw` library."""
        rotation = 90
        rotated = Rotate(
            self.pdf_path,
            rotation,
            suffix="rotated_90_pdfrw",
            tempdir=self.temp.name,
            method="pdfrw",
        ).file

        self.assertPdfExists(rotated)
        self.assertPdfRotation(rotated, rotation)

        expected_equals_output(function_name_to_file_name(), rotated)

    @Timer.decorator
    def test_rotate_pdfrw_180(self):
        """Rotate a PDF file by 180 degrees using the `pdfrw` library."""
        rotation = 180
        rotated = Rotate(
            self.pdf_path,
            rotation,
            suffix="rotated_180_pdfrw",
            tempdir=self.temp.name,
            method="pdfrw",
        ).file

        self.assertPdfExists(rotated)
        self.assertPdfRotation(rotated, rotation)

        expected_equals_output(function_name_to_file_name(), rotated)

    @Timer.decorator
    def test_rotate_pdfrw_270(self):
        """Rotate a PDF file by 270 degrees using the `pdfrw` library."""
        rotation = 270
        rotated = Rotate(
            self.pdf_path,
            rotation,
            suffix="rotated_270_pdfrw",
            tempdir=self.temp.name,
            method="pdfrw",
        ).file

        self.assertPdfExists(rotated)
        self.assertPdfRotation(rotated, rotation)

        expected_equals_output(function_name_to_file_name(), rotated)

    @Timer.decorator
    def test_rotate_pypdf3_90(self):
        """Rotate a PDF file by 90 degrees using the `pypdf3` library."""
        rotation = 90
        rotated = Rotate(
            self.pdf_path,
            rotation,
            suffix="rotated_90_pypdf3",
            tempdir=self.temp.name,
            method="pypdf3",
        ).file

        self.assertPdfExists(rotated)
        self.assertPdfRotation(rotated, rotation)

        expected_equals_output(function_name_to_file_name(), rotated)

    @Timer.decorator
    def test_rotate_pypdf3_180(self):
        """Rotate a PDF file by 180 degrees using the `pypdf3` library."""
        rotation = 180
        rotated = Rotate(
            self.pdf_path,
            rotation,
            suffix="rotated_180_pypdf3",
            tempdir=self.temp.name,
            method="pypdf3",
        ).file

        self.assertPdfExists(rotated)
        self.assertPdfRotation(rotated, rotation)

        expected_equals_output(function_name_to_file_name(), rotated)

    @Timer.decorator
    def test_rotate_pypdf3_270(self):
        """Rotate a PDF file by 270 degrees using the `pypdf3` library."""
        rotation = 270
        rotated = Rotate(
            self.pdf_path,
            rotation,
            suffix="rotated_270_pypdf3",
            tempdir=self.temp.name,
            method="pypdf3",
        ).file

        self.assertPdfExists(rotated)
        self.assertPdfRotation(rotated, rotation)

        expected_equals_output(function_name_to_file_name(), rotated)

    @Timer.decorator
    def test_rotate_pypdf_90(self):
        """Rotate a PDF file by 90 degrees using the `pypdf` library."""
        rotation = 90
        rotated = Rotate(
            self.pdf_path,
            rotation,
            suffix="rotated_90_pypdf",
            tempdir=self.temp.name,
            method="pypdf",
        ).file

        self.assertPdfExists(rotated)
        self.assertPdfRotation(rotated, rotation)

        expected_equals_output(function_name_to_file_name(), rotated)

    @Timer.decorator
    def test_rotate_pypdf_180(self):
        """Rotate a PDF file by 180 degrees using the `pypdf` library."""
        rotation = 180
        rotated = Rotate(
            self.pdf_path,
            rotation,
            suffix="rotated_180_pypdf",
            tempdir=self.temp.name,
            method="pypdf",
        ).file

        self.assertPdfExists(rotated)
        self.assertPdfRotation(rotated, rotation)

        expected_equals_output(function_name_to_file_name(), rotated)

    @Timer.decorator
    def test_rotate_pypdf_270(self):
        """Rotate a PDF file by 270 degrees using the `pypdf` library."""
        rotation = 270
        rotated = Rotate(
            self.pdf_path,
            rotation,
            suffix="rotated_270_pypdf",
            tempdir=self.temp.name,
            method="pypdf",
        ).file

        self.assertPdfExists(rotated)
        self.assertPdfRotation(rotated, rotation)

        expected_equals_output(function_name_to_file_name(), rotated)

    def assertPdfExists(self, pdf):
        # Assert rotated pdf file exists
        self.assertTrue(os.path.isfile(pdf))

    def assertPdfRotation(self, rotated, rotation):
        self.assertEqual(Info(rotated).rotate, rotation)


if __name__ == "__main__":
    unittest.main()
