import os
import unittest
from tempfile import NamedTemporaryFile

from looptools import Timer

from pdfconduit.conduit import Encrypt
from pdfconduit.utils import Info
from tests import *


class TestEncrypt(unittest.TestCase):
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

    @Timer.decorator
    def test_encrypt_printing(self):
        """Encrypt a PDF file and allow users to print."""
        encrypted = Encrypt(
            self.pdf_path,
            self.user_pw,
            self.owner_pw,
            allow_printing=True,
            output=self.temp.name,
            suffix='allow_printing',
        )

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

    @Timer.decorator
    def test_encrypt_128bit(self):
        """Encrypt PDF file with 128bit encryption."""
        encrypted = Encrypt(self.pdf_path,
                            self.user_pw,
                            self.owner_pw,
                            output=self.temp.name,
                            bit128=True,
                            suffix='128bit')

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

        # Assert standard security handler revision is 3
        self.assertEqual(security['/R'], 3)

    @Timer.decorator
    def test_encrypt_40bit(self):
        """Encrypt PDF file with 40bit encryption."""
        encrypted = Encrypt(self.pdf_path,
                            self.user_pw,
                            self.owner_pw,
                            output=self.temp.name,
                            bit128=False,
                            suffix='40bit')

        # Encrypted pdf security info
        security = Info(encrypted.output, self.user_pw).security

        # Assert that pdf file exists
        self.assertTrue(os.path.exists(encrypted.output))

        # Assert that pdf file is now encrypted
        self.assertTrue(Info(encrypted.output, self.user_pw).encrypted)

        # Confirm length (128 for 128bit encryption) is missing
        self.assertFalse('/Length' in security)

        # Assert pdf security value is -1852
        self.assertEqual(security['/P'], -1852)

        # Assert standard security handler revision is 2
        self.assertEqual(security['/R'], 2)

    @Timer.decorator
    def test_encrypt_128bit_allow_commenting(self):
        """Encrypt a PDF file but allow the user to add comments."""
        encrypted = Encrypt(self.pdf_path,
                            self.user_pw,
                            self.owner_pw,
                            output=self.temp.name,
                            allow_printing=False,
                            allow_commenting=True,
                            bit128=True,
                            suffix='128bit_allow_commenting')

        # Encrypted pdf security info
        security = Info(encrypted.output, self.user_pw).security

        # Assert that pdf file exists
        self.assertTrue(os.path.exists(encrypted.output))

        # Assert that pdf file is now encrypted
        self.assertTrue(Info(encrypted.output, self.user_pw).encrypted)

        # Assert pdf security value is -800
        self.assertEqual(security['/P'], -800)

    @Timer.decorator
    def test_encrypt_128bit_allow_printing_and_commenting(self):
        """Encrypt a PDF file but allow the user to add comments."""
        encrypted = Encrypt(self.pdf_path,
                            self.user_pw,
                            self.owner_pw,
                            output=self.temp.name,
                            allow_printing=True,
                            allow_commenting=True,
                            bit128=True,
                            suffix='128bit_allow_printing_and_commenting')

        # Encrypted pdf security info
        security = Info(encrypted.output, self.user_pw).security

        # Assert that pdf file exists
        self.assertTrue(os.path.exists(encrypted.output))

        # Assert that pdf file is now encrypted
        self.assertTrue(Info(encrypted.output, self.user_pw).encrypted)

        # Assert pdf security value is -1500
        self.assertEqual(security['/P'], -1500)

        # Assert encryption bit size is 128
        self.assertEqual(security['/Length'], 128)

        # Assert standard security handler revision is 3
        self.assertEqual(security['/R'], 3)

    @Timer.decorator
    def test_encrypt_40bit_allow_commenting(self):
        """Encrypt a PDF file but allow the user to add comments."""
        encrypted = Encrypt(self.pdf_path,
                            self.user_pw,
                            self.owner_pw,
                            output=self.temp.name,
                            allow_printing=False,
                            allow_commenting=True,
                            bit128=False,
                            suffix='40bit_allow_commenting')

        # Encrypted pdf security info
        security = Info(encrypted.output, self.user_pw).security

        # Assert that pdf file exists
        self.assertTrue(os.path.exists(encrypted.output))

        # Assert that pdf file is now encrypted
        self.assertTrue(Info(encrypted.output, self.user_pw).encrypted)

        # Assert pdf security value is -800
        self.assertEqual(security['/P'], -800)

        # Confirm length (128 for 128bit encryption) is missing
        self.assertFalse('/Length' in security)

        # Assert standard security handler revision is 2
        self.assertEqual(security['/R'], 2)

    @Timer.decorator
    def test_encrypt_40bit_allow_printing_and_commenting(self):
        """Encrypt a PDF file but allow the user to add comments."""
        encrypted = Encrypt(self.pdf_path,
                            self.user_pw,
                            self.owner_pw,
                            output=self.temp.name,
                            allow_printing=True,
                            allow_commenting=True,
                            bit128=False,
                            suffix='40bit_allow_printing_and_commenting')

        # Encrypted pdf security info
        security = Info(encrypted.output, self.user_pw).security

        # Assert that pdf file exists
        self.assertTrue(os.path.exists(encrypted.output))

        # Assert that pdf file is now encrypted
        self.assertTrue(Info(encrypted.output, self.user_pw).encrypted)

        # Assert pdf security value is -1500
        self.assertEqual(security['/P'], -1500)

        # Confirm length (128 for 128bit encryption) is missing
        self.assertFalse('/Length' in security)

        # Assert standard security handler revision is 2
        self.assertEqual(security['/R'], 2)

    @Timer.decorator
    def test_password_byte_string(self):
        """Encrypt a PDF file and allow users to print."""
        encrypted = Encrypt(
            self.pdf_path,
            self.user_pw,
            self.owner_pw,
            output=self.temp.name,
            suffix='byte_string',
        )

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

        # Assert standard security handler revision is 3
        self.assertEqual(security['/R'], 3)

        # Assert user & owner password byte string is correct
        self.assertEqual(
            security['/O'],
            b'\xd0H\xd1R\x9eS]\x18\x84\xcd8V6{\x18KJ\x90\xdf\x01\xe67\xd1n\xca\x06[\xafNd\x90\x0b'
        )





if __name__ == '__main__':
    unittest.main()
