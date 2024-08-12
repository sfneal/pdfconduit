import os
import unittest
from tempfile import TemporaryDirectory

from pdfconduit import Conduit, Info
from tests import pdf_path


class PdfconduitTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Encryption passwords
        cls.owner_pw = "foo"
        cls.user_pw = "baz"
        cls.pdf_path = pdf_path

    def setUp(self):
        self.temp = TemporaryDirectory()
        self.conduit = Conduit(self.pdf_path).set_output_directory(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

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
