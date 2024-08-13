import os
import unittest
from tempfile import TemporaryDirectory
from pdfconduit.utils.typing import Tuple, List

from parameterized import parameterized

from pdfconduit.watermark.watermark import Watermark
from pdfconduit.watermark.label import Label
from pdfconduit.utils import Info
from tests import *


def watermark_params() -> List[Tuple[str, str, bool, bool]]:
    return [
        # name, method, flatten, underneath
        ("pdfrw", "pdfrw", False, False),
        ("pdfrw_underneath", "pdfrw", False, True),
        ("pdfrw_overlay", "pdfrw", False, False),
        ("pdfrw_flattened", "pdfrw", True, False),
        ("pdfrw_flattened_underneath", "pdfrw", True, True),
        ("pypdf", "pypdf", False, False),
        ("pypdf_underneath", "pypdf", False, True),
        ("pypdf_overlay", "pypdf", False, False),
        ("pypdf_flattened", "pypdf", True, False),
        ("pypdf_flattened_underneath", "pypdf", True, True),
    ]


class TestWatermark(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdf_path = pdf_path

    def setUp(self):
        self.temp = TemporaryDirectory()
        self.address = "43 Indian Lane"
        self.town = "Franklin"
        self.state = "MA"
        self.rotate = 30
        self.owner_pw = "foo"
        self.user_pw = "baz"

    def tearDown(self):
        self.temp.cleanup()

    @parameterized.expand(watermark_params)
    def test_watermark(
        self, name: str, method: str, flatten: bool = False, underneath: bool = False
    ):
        watermarker = Watermark(
            self.pdf_path, use_receipt=False, open_file=False, tempdir=self.temp.name
        )
        watermark = watermarker.draw(
            text1=self.address,
            text2=str(self.town + ", " + self.state),
            opacity=0.08,
            rotate=self.rotate,
            flatten=flatten,
        )
        added = watermarker.add(
            self.pdf_path, watermark, method=method, underneath=underneath
        )

        self.assertPdfExists(watermark)
        self.assertPdfExists(added)
        self.assertPdfHasResources(added)

    def test_conduit_watermark_label(self):
        """Apply a watermark label to a PDF file."""
        label = os.path.basename(self.pdf_path)
        labeled = Label(
            self.pdf_path, label, tempdir=self.temp.name, suffix=None
        ).write(cleanup=False)

        self.assertPdfExists(labeled)
        self.assertPdfHasResources(labeled)

    def assertPdfExists(self, pdf):
        # Assert watermarked PDF file exists
        self.assertTrue(os.path.exists(pdf))

    def assertPdfHasResources(self, pdf):
        # Assert watermarked PDF has page resources
        self.assertTrue(Info(pdf).resources())


if __name__ == "__main__":
    unittest.main()
