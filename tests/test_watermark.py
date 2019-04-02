import unittest
import os
from tempfile import TemporaryDirectory
from looptools import Timer
from pdfconduit import Watermark, Info, Label
from tests import *


class TestWatermarkMethodsPdfrw(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdf_path = pdf_path

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.temp = TemporaryDirectory()
        self.address = '43 Indian Lane'
        self.town = 'Franklin'
        self.state = 'MA'
        self.rotate = 30
        self.owner_pw = 'foo'
        self.user_pw = 'baz'

    def tearDown(self):
        self.temp.cleanup()

    @Timer.decorator
    def test_watermark_pdfrw(self):
        """Apply a watermark to all pages of PDF using the `pdfrw` method."""
        w = Watermark(self.pdf_path, use_receipt=False, open_file=False, tempdir=self.temp.name)
        wtrmrk = w.draw(self.address, str(self.town + ', ' + self.state), opacity=0.08, rotate=self.rotate,
                        flatten=False)
        added = w.add(self.pdf_path, wtrmrk, method='pdfrw', suffix='watermarked_pdfrw')

        # Assert the watermark file exists
        self.assertTrue(os.path.exists(wtrmrk))

        # Assert watermarked PDF file exists
        self.assertTrue(os.path.exists(added))

        # Assert watermarked PDF has page resources
        self.assertTrue(Info(added).resources())
        return added

    def test_watermark_underneath_pdfrw(self):
        """Apply a watermark underneath original content of PDF using the `pdfrw` method."""
        w = Watermark(self.pdf_path, use_receipt=False, open_file=False, tempdir=self.temp.name)
        wtrmrk = w.draw(self.address, str(self.town + ', ' + self.state), opacity=0.08, rotate=self.rotate)
        added = w.add(self.pdf_path, wtrmrk, underneath=True, suffix='watermarked_underneath_pdfrw', method='pdfrw')

        # Assert the watermark file exists
        self.assertTrue(os.path.exists(wtrmrk))

        # Assert watermarked PDF file exists
        self.assertTrue(os.path.exists(added))

        # Assert watermarked PDF has page resources
        self.assertTrue(Info(added).resources())
        return added

    def test_watermark_overlay_pdfrw(self):
        """Apply a watermark overlaid over original content of PDF using the `pdfrw` method."""
        w = Watermark(self.pdf_path, use_receipt=False, open_file=False, tempdir=self.temp.name)
        wtrmrk = w.draw(self.address, str(self.town + ', ' + self.state), opacity=0.08, rotate=self.rotate)
        added = w.add(self.pdf_path, wtrmrk, underneath=False, suffix='watermarked_overlay_pdfrw', method='pdfrw')

        # Assert the watermark file exists
        self.assertTrue(os.path.exists(wtrmrk))

        # Assert watermarked PDF file exists
        self.assertTrue(os.path.exists(added))

        # Assert watermarked PDF has page resources
        self.assertTrue(Info(added).resources())
        return added

    def test_watermark_flat_pdfrw(self):
        """Apply a flattened watermark to a PDF using the `pdfrw` method."""
        w = Watermark(self.pdf_path, use_receipt=False, open_file=False, tempdir=self.temp.name)
        flat = w.draw(self.address, str(self.town + ', ' + self.state), opacity=0.08, flatten=True)
        added = w.add(self.pdf_path, flat, suffix='watermarked_flat_pdfrw', method='pdfrw')

        # Assert the watermark file exists
        self.assertTrue(os.path.exists(flat))

        # Assert watermarked PDF file exists
        self.assertTrue(os.path.exists(added))

        # Assert watermarked PDF has page resources
        self.assertTrue(Info(added).resources())
        return added

    def test_watermark_layered_pdfrw(self):
        """Apply a flattened watermark to a PDF using the `pdfrw` method."""
        w = Watermark(self.pdf_path, use_receipt=False, open_file=False, tempdir=self.temp.name)
        layered = w.draw(self.address, str(self.town + ', ' + self.state), opacity=0.08, flatten=False)
        added = w.add(self.pdf_path, layered, suffix='watermarked_layered_pdfrw', method='pdfrw')

        # Assert the watermark file exists
        self.assertTrue(os.path.exists(layered))

        # Assert watermarked PDF file exists
        self.assertTrue(os.path.exists(added))

        # Assert watermarked PDF has page resources
        self.assertTrue(Info(added).resources())
        return added

    def test_watermark_label(self):
        """Apply a watermark label to a PDF file."""
        w = Watermark(self.pdf_path, use_receipt=False, open_file=False, tempdir=self.temp.name)
        label = os.path.basename(self.pdf_path)
        labeled = Label(self.pdf_path, label, tempdir=self.temp.name).write(cleanup=False)

        # Assert the watermark file exists
        self.assertTrue(os.path.exists(label))

        # Assert watermarked PDF file exists
        self.assertTrue(os.path.exists(labeled))

        # Assert watermarked PDF has page resources
        self.assertTrue(Info(labeled).resources())
        return labeled


if __name__ == '__main__':
    unittest.main()
