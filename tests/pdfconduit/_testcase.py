import unittest
from tempfile import TemporaryDirectory

from pdfconduit import Conduit
from tests import pdf_path


class PdfconduitTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Encryption passwords
        cls.owner_pw = "foo"
        cls.user_pw = "baz"
        cls.pdf_path = pdf_path

    def setUp(self):
        self.temp = TemporaryDirectory(delete=False)
        self.conduit = Conduit(self.pdf_path).set_output_directory(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()
