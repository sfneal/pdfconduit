import unittest
from tempfile import NamedTemporaryFile
from pdfconduit import Encrypt, Info
from tests import *


class TestEncrypt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Encryption passwords
        cls.owner_pw = 'foo'
        cls.user_pw = 'baz'
        cls.pdf_path = pdf_path

    def setUp(self):
        self.temp = NamedTemporaryFile(suffix='.pdf')

    def test_encrypt_printing(self):
        p = Encrypt(self.pdf_path, self.user_pw, self.owner_pw, output=self.temp.name, suffix='secured')
        security = Info(p.output, self.user_pw).security

        self.assertTrue(Info(p.output, self.user_pw).encrypted)
        self.assertEqual(security['/Length'], 128)
        self.assertEqual(security['/P'], -1852)

    def test_encrypt_128bit(self):
        p = Encrypt(self.pdf_path, self.user_pw, self.owner_pw, output=self.temp.name, bit128=True,
                    suffix='secured_128bit')
        security = Info(p.output, self.user_pw).security

        self.assertTrue(Info(p.output, self.user_pw).encrypted)
        self.assertEqual(security['/Length'], 128)

    def test_encrypt_40bit(self):
        p = Encrypt(self.pdf_path, self.user_pw, self.owner_pw, output=self.temp.name, bit128=False,
                    suffix='secured_40bit')

        self.assertTrue(Info(p.output, self.user_pw).encrypted)

    def test_encrypt_commenting(self):
        p = Encrypt(self.pdf_path, self.user_pw, self.owner_pw, output=self.temp.name, allow_commenting=True,
                    suffix='secured_commenting')
        security = Info(p.output, self.user_pw).security

        self.assertTrue(Info(p.output, self.user_pw).encrypted)
        self.assertEqual(security['/P'], -1500)


if __name__ == '__main__':
    unittest.main()
