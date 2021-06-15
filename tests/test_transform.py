import os
import unittest
from tempfile import TemporaryDirectory

from looptools import Timer

from pdfconduit import Info, Merge, Upscale, Rotate, slicer
from tests import *


class TestTransformMerge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdfs = [os.path.join(test_data_dir, p) for p in ['article.pdf', 'charts.pdf', 'document.pdf', 'manual.pdf']]

    def setUp(self):
        self.temp = TemporaryDirectory()

    def tearDown(self):
        self.temp.cleanup()

    @Timer.decorator
    def test_merge_pypdf3(self):
        """Merge multiple PDF files into a single PDF using the `PyPDF3` library."""
        merged = Merge(self.pdfs, output_name='merged_pypdf3', output_dir=self.temp.name, method='pypdf3')

        # Assert merged file exists
        self.assertTrue(os.path.exists(merged.file))

        # Assert sum of pages in original pdf files equals sum of pages in merged pdf
        self.assertEqual(sum([Info(pdf).pages for pdf in self.pdfs]), Info(merged.file).pages)
        return merged

    @Timer.decorator
    def test_merge_pdfrw(self):
        """Merge multiple PDF files into a single PDF using the `pdfrw` library."""
        merged = Merge(self.pdfs, output_name='merged_pdfrw', output_dir=self.temp.name, method='pdfrw')

        # Assert merged file exists
        self.assertTrue(os.path.exists(merged.file))

        # Assert sum of pages in original pdf files equals sum of pages in merged pdf
        self.assertEqual(sum([Info(pdf).pages for pdf in self.pdfs]), Info(merged.file).pages)
        return merged


class TestTransformUpscale(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdf_path = pdf_path
        cls.temp = TemporaryDirectory()

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    @Timer.decorator
    def test_upscale_pdfrw_20x(self):
        """Resize a PDF file to 2.0x times the original scale."""
        s = 2.0
        upscaled = Upscale(pdf_path, scale=s, suffix='upscaled_2.0_pdfrw', tempdir=self.temp.name, method='pdfrw').file

        # Assert upscaled file exists
        self.assertTrue(os.path.isfile(upscaled))

        # Assert upscaled pdf file is the correct size
        self.assertEqual(Info(upscaled).size, tuple([i * s for i in Info(pdf_path).size]))
        return upscaled

    @Timer.decorator
    def test_upscale_pdfrw_15x(self):
        """Resize a PDF file to 1.5x times the original scale."""
        s = 1.5
        upscaled = Upscale(pdf_path, scale=s, suffix='upscaled_1.5_pdfrw', tempdir=self.temp.name, method='pdfrw').file

        # Assert upscaled file exists
        self.assertTrue(os.path.isfile(upscaled))

        # Assert upscaled pdf file is the correct size
        self.assertEqual(Info(upscaled).size, tuple([i * s for i in Info(pdf_path).size]))
        return upscaled

    @Timer.decorator
    def test_upscale_pdfrw_30x(self):
        """Resize a PDF file to 3.0x times the original scale."""
        s = 3.0
        upscaled = Upscale(pdf_path, scale=s, suffix='upscaled_3.0_pdfrw', tempdir=self.temp.name, method='pdfrw').file

        # Assert upscaled file exists
        self.assertTrue(os.path.isfile(upscaled))

        # Assert upscaled pdf file is the correct size
        self.assertEqual(Info(upscaled).size, tuple([i * s for i in Info(pdf_path).size]))
        return upscaled

    @Timer.decorator
    def test_downscale_pdfrw_20x(self):
        """Resize a PDF file to 3.0x times the original scale."""
        s = 1 / 2
        upscaled = Upscale(pdf_path, scale=s, suffix='downscaled_2.0_pdfrw', tempdir=self.temp.name,
                           method='pdfrw').file

        # Assert upscaled file exists
        self.assertTrue(os.path.isfile(upscaled))

        # Assert upscaled pdf file is the correct size
        self.assertEqual(Info(upscaled).size, tuple([i * s for i in Info(pdf_path).size]))
        return upscaled


class TestTransformSlice(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdf_path = pdf_path

    def setUp(self):
        self.temp = TemporaryDirectory()

    def tearDown(self):
        self.temp.cleanup()

    @Timer.decorator
    def test_slice(self):
        """Slice a page range from a PDF to create a new 'trimmed' pdf file."""
        fp = 1
        lp = 1
        sliced = slicer(self.pdf_path, first_page=fp, last_page=lp, tempdir=self.temp.name)

        # Assert sliced file exists
        self.assertTrue(os.path.isfile(sliced))

        # Confirm slicer sliced the correct number of pages
        self.assertEqual(Info(sliced).pages, len(range(fp, lp + 1)))
        return sliced

    @Timer.decorator
    def test_slice2(self):
        """Slice a page range from a PDF to create a new 'trimmed' pdf file."""
        fp = 4
        lp = 7
        sliced = slicer(self.pdf_path, first_page=fp, last_page=lp, tempdir=self.temp.name)

        # Assert sliced file exists
        self.assertTrue(os.path.isfile(sliced))

        # Confirm slicer sliced the correct number of pages
        self.assertEqual(Info(sliced).pages, len(range(fp, lp + 1)))
        return sliced


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
        rotated = Rotate(self.pdf_path, rotation, suffix='rotated_pdfrw', tempdir=self.temp.name, method='pdfrw').file

        # Assert rotated pdf file exists
        self.assertTrue(os.path.isfile(rotated))

        # Assert pdf file was rotated by the correct amount of degrees
        self.assertEqual(Info(rotated).rotate, rotation)
        return rotated

    @Timer.decorator
    def test_rotate_pdfrw_180(self):
        """Rotate a PDF file by 180 degrees using the `pdfrw` library."""
        rotation = 180
        rotated = Rotate(self.pdf_path, rotation, suffix='rotated_180_pdfrw', tempdir=self.temp.name,
                         method='pdfrw').file

        # Assert rotated pdf file exists
        self.assertTrue(os.path.isfile(rotated))

        # Assert pdf file was rotated by the correct amount of degrees
        self.assertEqual(Info(rotated).rotate, rotation)
        return rotated

    @Timer.decorator
    def test_rotate_pdfrw_270(self):
        """Rotate a PDF file by 270 degrees using the `pdfrw` library."""
        rotation = 270
        rotated = Rotate(self.pdf_path, rotation, suffix='rotated_270_pdfrw', tempdir=self.temp.name,
                         method='pdfrw').file

        # Assert rotated pdf file exists
        self.assertTrue(os.path.isfile(rotated))

        # Assert pdf file was rotated by the correct amount of degrees
        self.assertEqual(Info(rotated).rotate, rotation)
        return rotated

    @Timer.decorator
    def test_rotate_pypdf3_90(self):
        """Rotate a PDF file by 90 degrees using the `pypdf3` library."""
        rotation = 90
        rotated = Rotate(self.pdf_path, rotation, suffix='rotated_pdfrw', tempdir=self.temp.name, method='pypdf3').file

        # Assert rotated pdf file exists
        self.assertTrue(os.path.isfile(rotated))

        # Assert pdf file was rotated by the correct amount of degrees
        self.assertEqual(Info(rotated).rotate, rotation)
        return rotated

    @Timer.decorator
    def test_rotate_pypdf3_180(self):
        """Rotate a PDF file by 180 degrees using the `pypdf3` library."""
        rotation = 180
        rotated = Rotate(self.pdf_path, rotation, suffix='rotated_180_pdfrw', tempdir=self.temp.name,
                         method='pypdf3').file

        # Assert rotated pdf file exists
        self.assertTrue(os.path.isfile(rotated))

        # Assert pdf file was rotated by the correct amount of degrees
        self.assertEqual(Info(rotated).rotate, rotation)
        return rotated

    @Timer.decorator
    def test_rotate_pypdf3_270(self):
        """Rotate a PDF file by 270 degrees using the `pypdf3` library."""
        rotation = 270
        rotated = Rotate(self.pdf_path, rotation, suffix='rotated_270_pdfrw', tempdir=self.temp.name,
                         method='pypdf3').file

        # Assert rotated pdf file exists
        self.assertTrue(os.path.isfile(rotated))

        # Assert pdf file was rotated by the correct amount of degrees
        self.assertEqual(Info(rotated).rotate, rotation)
        return rotated


if __name__ == '__main__':
    unittest.main()
