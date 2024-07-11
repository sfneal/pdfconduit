import os
import unittest
from tempfile import TemporaryDirectory

from looptools import Timer

from pdfconduit import Info, Upscale
from tests import *


class TestUpscale(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdf_path = pdf_path
        cls.temp = TemporaryDirectory()

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    @Timer.decorator
    def test_upscale_pdfrw_20x(self):
        s = 2.0
        upscaled = (
            Upscale(
                pdf_path,
                scale=s,
                suffix="upscaled_2.0_pdfrw",
                tempdir=self.temp.name,
            )
            .use_pdfrw()
            .upscale()
        )

        self.assertPdfExists(upscaled)
        self.assertPdfUpscaled(s, upscaled)

        expected_equals_output(function_name_to_file_name(), upscaled)

    @Timer.decorator
    def test_upscale_pdfrw_15x(self):
        s = 1.5
        upscaled = (
            Upscale(
                pdf_path,
                scale=s,
                suffix="upscaled_1.5_pdfrw",
                tempdir=self.temp.name,
            )
            .use_pdfrw()
            .upscale()
        )

        self.assertPdfExists(upscaled)
        self.assertPdfUpscaled(s, upscaled)

        expected_equals_output(function_name_to_file_name(), upscaled)

    @Timer.decorator
    def test_upscale_pdfrw_30x(self):
        s = 3.0
        upscaled = (
            Upscale(
                pdf_path,
                scale=s,
                suffix="upscaled_3.0_pdfrw",
                tempdir=self.temp.name,
            )
            .use_pdfrw()
            .upscale()
        )

        self.assertPdfExists(upscaled)
        self.assertPdfUpscaled(s, upscaled)

        expected_equals_output(function_name_to_file_name(), upscaled)

    @Timer.decorator
    def test_downscale_pdfrw_20x(self):
        s = 1 / 2
        upscaled = (
            Upscale(
                pdf_path,
                scale=s,
                suffix="downscaled_2.0_pdfrw",
                tempdir=self.temp.name,
            )
            .use_pdfrw()
            .upscale()
        )

        self.assertPdfExists(upscaled)
        self.assertPdfUpscaled(s, upscaled)

        expected_equals_output(function_name_to_file_name(), upscaled)

    @Timer.decorator
    def test_upscale_pypdf_20x(self):
        s = 2.0
        upscaled = (
            Upscale(
                pdf_path,
                scale=s,
                suffix="upscaled_2.0_pypdf",
                tempdir=self.temp.name,
            )
            .use_pypdf()
            .upscale()
        )

        self.assertPdfExists(upscaled)
        self.assertPdfUpscaled(s, upscaled)

        expected_equals_output(function_name_to_file_name(), upscaled)

    @Timer.decorator
    def test_upscale_pypdf_15x(self):
        s = 1.5
        upscaled = (
            Upscale(
                pdf_path,
                scale=s,
                suffix="upscaled_1.5_pypdf",
                tempdir=self.temp.name,
            )
            .use_pypdf()
            .upscale()
        )

        self.assertPdfExists(upscaled)
        self.assertPdfUpscaled(s, upscaled)

        expected_equals_output(function_name_to_file_name(), upscaled)

    @Timer.decorator
    def test_upscale_pypdf_30x(self):
        s = 3.0
        upscaled = (
            Upscale(
                pdf_path,
                scale=s,
                suffix="upscaled_3.0_pypdf",
                tempdir=self.temp.name,
            )
            .use_pypdf()
            .upscale()
        )

        self.assertPdfExists(upscaled)
        self.assertPdfUpscaled(s, upscaled)

        expected_equals_output(function_name_to_file_name(), upscaled)

    @Timer.decorator
    def test_downscale_pypdf_20x(self):
        s = 1 / 2
        upscaled = (
            Upscale(
                pdf_path,
                scale=s,
                suffix="downscaled_2.0_pypdf",
                tempdir=self.temp.name,
            )
            .use_pypdf()
            .upscale()
        )

        self.assertPdfExists(upscaled)
        self.assertPdfUpscaled(s, upscaled)

        expected_equals_output(function_name_to_file_name(), upscaled)

    def assertPdfUpscaled(self, s, upscaled):
        self.assertEqual(
            Info(upscaled).size, tuple([i * s for i in Info(pdf_path).size])
        )
        self.assertEqual(Info(upscaled).pages, Info(pdf_path).pages)

    def assertPdfExists(self, upscaled):
        self.assertTrue(os.path.isfile(upscaled))


if __name__ == "__main__":
    unittest.main()
