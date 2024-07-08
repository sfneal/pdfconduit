import unittest

from PyPDF3 import PdfFileReader
from PyPDF3.utils import PdfReadError
from looptools import Timer

from pdfconduit.utils import pypdf3_reader
from tests import *


class TestRead(unittest.TestCase):
    @Timer.decorator
    def test_pypdf3_reader_can_read_unencrypted(self):
        file_path = test_data_path("document.pdf")
        reader = pypdf3_reader(file_path)

        self.assertIsInstance(reader, PdfFileReader)
        self.assertEqual(reader.getNumPages(), 11)

    @Timer.decorator
    def test_pypdf3_reader_cant_read_encrypted(self):
        file_path = test_data_path("encrypted.pdf")
        reader = pypdf3_reader(file_path)

        with self.assertRaises(PdfReadError) as context:
            reader.getNumPages()

        self.assertIsInstance(context.exception, PdfReadError)
        self.assertEqual("File has not been decrypted", context.exception.__str__())

    @Timer.decorator
    def test_pypdf3_reader_can_read_encrypted_with_password(self):
        file_path = test_data_path("encrypted.pdf")
        reader = pypdf3_reader(file_path, "foo")

        self.assertIsInstance(reader, PdfFileReader)
        self.assertTrue(reader.isEncrypted)
        self.assertEqual(reader.getNumPages(), 11)


if __name__ == "__main__":
    unittest.main()
