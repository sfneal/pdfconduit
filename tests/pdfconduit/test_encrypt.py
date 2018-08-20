import unittest
import os
from pdfconduit import Encrypt, Info
from tests import pdf, directory


class TestEncrypt(unittest.TestCase):
    def setUp(self):
        self.owner_pw = 'foo'
        self.user_pw = 'baz'

    def test_encrypt(self):
        p = Encrypt(pdf, self.user_pw, self.owner_pw)
        security = Info(p.output, self.user_pw).security

        self.assertTrue(Info(p.output, self.user_pw).encrypted)
        self.assertEqual(security['/Length'], 128)
        self.assertEqual(security['/P'], -1852)

    def test_encrypt_128bit(self):
        p = Encrypt(pdf, self.user_pw, self.owner_pw, bit128=True)
        security = Info(p.output, self.user_pw).security

        self.assertTrue(Info(p.output, self.user_pw).encrypted)
        self.assertEqual(security['/Length'], 128)

    def test_encrypt_40bit(self):
        p = Encrypt(pdf, self.user_pw, self.owner_pw, bit128=False)

        self.assertTrue(Info(p.output, self.user_pw).encrypted)

    def test_encrypt_commenting(self):
        p = Encrypt(pdf, self.user_pw, self.owner_pw, allow_commenting=True)
        security = Info(p.output, self.user_pw).security

        self.assertTrue(Info(p.output, self.user_pw).encrypted)
        self.assertEqual(security['/P'], -1500)

    def test_encrypt_pflag(self):
        _range = [-(x + 50) for x in range(0, 1852)[::100]]
        for i in _range:
            p = Encrypt(pdf, self.user_pw, self.owner_pw, output=os.path.join(directory, 'P', str(i) + '.pdf'),
                        overwrite_permission=i)
            security = Info(p.output, self.user_pw).security

            self.assertTrue(Info(p.output, self.user_pw).encrypted)
            self.assertEqual(security['/Length'], 128)
            self.assertEqual(security['/P'], i)


if __name__ == '__main__':
    unittest.main()
