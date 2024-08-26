import os
import warnings
from io import BufferedReader

from pypdf import PdfReader, PdfWriter

from pdfconduit import Pdfconduit
from pdfconduit.utils import add_suffix
from tests import *
from tests import PdfconduitTestCase


class TestUsage(PdfconduitTestCase):
    def test_can_use_context_manager(self):
        with Pdfconduit(self.pdf_path) as conduit:
            conduit.set_output_directory(self.temp.name)

            self.assertIsInstance(conduit._pdf_file, BufferedReader)
            self.assertIsInstance(conduit._reader, PdfReader)
            self.assertIsInstance(conduit._writer, PdfWriter)
            self.assertIsNone(conduit.output)

        self.assertIsInstance(conduit.output, str)
        self.assertTrue(os.path.exists(conduit.output))

    def test_can_read_unencrypted_pdf(self):
        conduit = Pdfconduit(self.pdf_path)

        self.assertIsInstance(conduit._pdf_file, BufferedReader)
        self.assertIsInstance(conduit._reader, PdfReader)

    def test_can_read_encrypted_pdf(self):
        conduit = Pdfconduit(test_data_path("encrypted.pdf"), self.user_pw)

        self.assertIsInstance(conduit._pdf_file, BufferedReader)
        self.assertIsInstance(conduit._reader, PdfReader)

    def test_can_set_default_metadata(self):
        original = self.conduit.info.metadata

        self.assertNotEqual("pdfconduit", original.producer)
        self.assertNotEqual("pdfconduit", original.creator)
        self.assertNotEqual("pdfconduit", original.author)

        self.conduit.write()

        self.assertNotEqual(original, self.conduit.info.metadata)
        self.assertEqual("pdfconduit", self.conduit.info.metadata.producer)
        self.assertEqual("pdfconduit", self.conduit.info.metadata.creator)
        self.assertEqual("pdfconduit", self.conduit.info.metadata.author)

    def test_can_set_custom_metadata(self):
        original = self.conduit.info.metadata
        self.conduit.set_metadata({"/Producer": "Big Dom"})
        self.conduit.write()

        self.assertNotEqual(original, self.conduit.info.metadata)
        self.assertEqual("Big Dom", self.conduit.info.metadata.producer)

    def test_can_set_output(self):
        self.assertEqual(self.conduit._output_dir, self.temp.name)
        self.conduit.write()
        self.assertEqual(os.path.dirname(self.conduit.output), self.temp.name)

    def test_can_set_output_suffix(self):
        self.conduit = Pdfconduit(self.pdf_path)
        self.conduit.set_output_suffix("changed")
        output = add_suffix(self.pdf_path, "changed")
        self.assertEqual(output, self.conduit.output)

    def test_can_read_from_stream(self):
        conduit = Pdfconduit(self._get_pdf_byte_stream())

        self.assertIsNone(conduit._pdf_file)
        self.assertIsInstance(conduit._reader, PdfReader)
        self.assertIsInstance(conduit._writer, PdfWriter)

    def test_can_read_from_stream_and_write_to_file(self):
        output = os.path.join(self.temp.name, "streamed.pdf")
        conduit = Pdfconduit(self._get_pdf_byte_stream()).set_output(output)

        self.assertIsNone(conduit._pdf_file)
        self.assertIsInstance(conduit._reader, PdfReader)
        self.assertIsInstance(conduit._writer, PdfWriter)

        conduit.write()

        self.assertPdfExists(output)

    def test_can_write_stream_to_file_without_output(self):
        conduit = Pdfconduit(self._get_pdf_byte_stream())

        self.assertIsNone(conduit._pdf_file)
        self.assertIsInstance(conduit._reader, PdfReader)
        self.assertIsInstance(conduit._writer, PdfWriter)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            conduit.write()

            self.assertPdfExists(conduit.output)

            assert len(w) == 1
            assert issubclass(w[-1].category, UserWarning)
            assert "Saving PDFs to a temporary directory because" in str(w[-1].message)

    def test_can_set_temp_output(self):
        self.conduit = Pdfconduit(self.pdf_path)
        self.conduit.set_output_temp()
        self.conduit.write()
        self.assertPdfExists(self.conduit.output)

        self.conduit.cleanup()
        self.assertPdfDoesntExists(self.conduit.output)
