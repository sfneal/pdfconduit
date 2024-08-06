import os
from io import BufferedReader

from pypdf import PdfReader, PdfWriter

from pdfconduit import Conduit
from pdfconduit.utils import add_suffix
from tests import *
from tests.pdfconduit import PdfconduitTestCase


class TestUsage(PdfconduitTestCase):
    def test_can_use_context_manager(self):
        with Conduit(self.pdf_path) as conduit:
            conduit.set_output_directory(self.temp.name)
            
            self.assertIsInstance(conduit._pdf_file, BufferedReader)
            self.assertIsInstance(conduit._reader, PdfReader)
            self.assertIsInstance(conduit._writer, PdfWriter)
            self.assertIsNone(conduit.output)

        self.assertIsInstance(conduit.output, str)
        self.assertTrue(os.path.exists(conduit.output))

    def test_can_read_unencrypted_pdf(self):
        conduit = Conduit(self.pdf_path)

        self.assertIsInstance(conduit._pdf_file, BufferedReader)
        self.assertIsInstance(conduit._reader, PdfReader)

    def test_can_read_encrypted_pdf(self):
        conduit = Conduit(test_data_path('encrypted.pdf'), self.user_pw)

        self.assertIsInstance(conduit._pdf_file, BufferedReader)
        self.assertIsInstance(conduit._reader, PdfReader)

    def test_can_set_default_metadata(self):
        original = self.conduit.info.metadata

        self.assertNotEqual('pdfconduit', original.producer)
        self.assertNotEqual('pdfconduit', original.creator)
        self.assertNotEqual('pdfconduit', original.author)

        self.conduit.write()

        self.assertNotEqual(original, self.conduit.info.metadata)
        self.assertEqual('pdfconduit', self.conduit.info.metadata.producer)
        self.assertEqual('pdfconduit', self.conduit.info.metadata.creator)
        self.assertEqual('pdfconduit', self.conduit.info.metadata.author)

    def test_can_set_custom_metadata(self):
        original = self.conduit.info.metadata
        self.conduit.set_metadata({
            '/Producer': 'Big Dom'
        })
        self.conduit.write()

        self.assertNotEqual(original, self.conduit.info.metadata)
        self.assertEqual('Big Dom', self.conduit.info.metadata.producer)

    def test_can_set_output(self):
        self.assertEqual(self.conduit._output_dir, self.temp.name)
        self.conduit.write()
        self.assertEqual(os.path.dirname(self.conduit.output), self.temp.name)

    def test_can_set_output_suffix(self):
        self.conduit = Conduit(self.pdf_path)
        self.conduit.set_output_suffix('changed')
        output = add_suffix(self.pdf_path, 'changed')
        self.assertEqual(output, self.conduit.output)

    # def test_can_encrypt_pdf(self):
    #     pass
    #
    # def test_can_merge_pdf(self):
    #     pass
    #
    # def test_can_rotate_pdf(self):
    #     pass
    #
    # def test_can_scale_pdf(self):
    #     pass
    #
    # def test_can_flatten_pdf(self):
    #     pass
    #
    # def test_can_remove_duplications_from_pdf(self):
    #     pass
    #
    # def test_can_remove_images_from_pdf(self):
    #     pass
    #
    # def test_can_reduce_image_quality_of_pdf(self):
    #     pass
    #
    # def test_can_compress_pdf(self):
    #     pass
    #
    # def test_can_get_pdf_info(self):
    #     pass


