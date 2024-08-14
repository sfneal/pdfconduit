import os
import unittest
from tempfile import TemporaryDirectory
from typing import Tuple, List

from parameterized import parameterized

from pdfconduit import Info, Label, Watermark
from tests import *


def watermark_params() -> List[Tuple[str, str, bool, bool]]:
    return [
        # name, method, flatten, underneath
        ("basic", "pdfrw", False, False),
        ("underneath", "pdfrw", False, True),
        ("overlay", "pdfrw", False, False),
        ("flattened", "pdfrw", True, False),
        ("flattened_underneath", "pdfrw", True, True),
        ("basic", "pypdf", False, False),
        ("underneath", "pypdf", False, True),
        ("overlay", "pypdf", False, False),
        ("flattened", "pypdf", True, False),
        ("flattened_underneath", "pypdf", True, True),
    ]


def encryption_name_func(testcase_func, param_num, param):
    return "{}.{}.{}".format(testcase_func.__name__, param.args[0], param.args[1])


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

    @parameterized.expand(watermark_params, name_func=encryption_name_func)
    def test_watermark(
        self, name: str, method: str, flatten: bool = False, underneath: bool = False
    ):
        watermarker = Watermark(self.pdf_path, use_receipt=True, tempdir=self.temp.name)
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
