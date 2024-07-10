import unittest

from pypdf import PdfReader
from pypdf.errors import PdfReadError
from looptools import Timer
from pdfconduit.utils import pypdf_reader

from tests import *


class TestRead(unittest.TestCase):
    @Timer.decorator
    def test_pypdf_reader_can_read_unencrypted(self):
        file_path = test_data_path("document.pdf")
        reader = pypdf_reader(file_path)

        self.assertIsInstance(reader, PdfReader)
        self.assertEqual(reader.get_num_pages(), 11)

    @Timer.decorator
    def test_pypdf_reader_cant_read_encrypted(self):
        file_path = test_data_path("encrypted.pdf")
        reader = pypdf_reader(file_path)

        with self.assertRaises(PdfReadError) as context:
            reader.get_num_pages()

        self.assertIsInstance(context.exception, PdfReadError)
        self.assertEqual("File has not been decrypted", context.exception.__str__())

    @Timer.decorator
    def test_pypdf_reader_can_read_encrypted_with_password(self):
        file_path = test_data_path("encrypted.pdf")
        reader = pypdf_reader(file_path, "foo")

        self.assertIsInstance(reader, PdfReader)
        self.assertTrue(reader.is_encrypted)
        self.assertEqual(reader.get_num_pages(), 11)


if __name__ == "__main__":
    unittest.main()
