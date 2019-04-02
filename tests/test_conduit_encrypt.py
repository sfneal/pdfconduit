import os
import unittest
from tempfile import NamedTemporaryFile

from pdfconduit import Encrypt, Info
from tests import *


class TestConduitEncrypt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Encryption passwords
        cls.owner_pw = 'foo'
        cls.user_pw = 'baz'
        cls.pdf_path = pdf_path

    def setUp(self):
        self.temp = NamedTemporaryFile(suffix='.pdf', delete=False)

    def tearDown(self):
        if os.path.exists(self.temp.name):
            os.remove(self.temp.name)

    def test_conduit_encrypt_printing(self):
        """Encrypt a PDF file and allow users to print."""
        encrypted = Encrypt(self.pdf_path, self.user_pw, self.owner_pw, output=self.temp.name, suffix='secured')

        # Encrypted pdf security info
        security = Info(encrypted.output, self.user_pw).security

        # Assert that pdf file exists
        self.assertTrue(os.path.exists(encrypted.output))

        # Assert that pdf file is now encrypted
        self.assertTrue(Info(encrypted.output, self.user_pw).encrypted)

        # Assert encryption bit size is 128
        self.assertEqual(security['/Length'], 128)

        # Assert pdf security value is -1852
        self.assertEqual(security['/P'], -1852)

    def test_conduit_encrypt_128bit(self):
        """Encrypt PDF file with 128bit encryption."""
        encrypted = Encrypt(self.pdf_path, self.user_pw, self.owner_pw, output=self.temp.name, bit128=True,
                            suffix='secured_128bit')

        # Encrypted pdf security info
        security = Info(encrypted.output, self.user_pw).security

        # Assert that pdf file exists
        self.assertTrue(os.path.exists(encrypted.output))

        # Assert that pdf file is now encrypted
        self.assertTrue(Info(encrypted.output, self.user_pw).encrypted)

        # Assert encryption bit size is 128
        self.assertEqual(security['/Length'], 128)

    def test_conduit_encrypt_40bit(self):
        """Encrypt PDF file with 40bit encryption."""
        encrypted = Encrypt(self.pdf_path, self.user_pw, self.owner_pw, output=self.temp.name, bit128=False,
                            suffix='secured_40bit')

        # Encrypted pdf security info
        security = Info(encrypted.output, self.user_pw).security

        # Assert that pdf file exists
        self.assertTrue(os.path.exists(encrypted.output))

        # Assert that pdf file is now encrypted
        self.assertTrue(Info(encrypted.output, self.user_pw).encrypted)

        # Assert pdf security value is -1852
        self.assertEqual(security['/P'], -1852)

    def test_conduit_encrypt_commenting(self):
        """Encrypt a PDF file but allow the user to add comments."""
        encrypted = Encrypt(self.pdf_path, self.user_pw, self.owner_pw, output=self.temp.name, allow_commenting=True,
                            suffix='secured_commenting')

        # Encrypted pdf security info
        security = Info(encrypted.output, self.user_pw).security

        # Assert that pdf file exists
        self.assertTrue(os.path.exists(encrypted.output))

        # Assert that pdf file is now encrypted
        self.assertTrue(Info(encrypted.output, self.user_pw).encrypted)

        # Assert pdf security value is -1500
        self.assertEqual(security['/P'], -1500)


if __name__ == '__main__':
    unittest.main()
