import os
import unittest
from tempfile import NamedTemporaryFile

from looptools import Timer

from pdfconduit.conduit import Encrypt
from pdfconduit.conduit.encrypt import Algorithms
from pdfconduit.utils import Info
from tests import *


class TestEncrypt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Encryption passwords
        cls.owner_pw = "foo"
        cls.user_pw = "baz"
        cls.pdf_path = pdf_path

    def setUp(self):
        self.temp = NamedTemporaryFile(suffix=".pdf", delete=False)

    def tearDown(self):
        if os.path.exists(self.temp.name):
            os.remove(self.temp.name)

    @Timer.decorator
    def test_encrypt_128bit(self):
        encrypted = Encrypt(
            self.pdf_path,
            self.user_pw,
            self.owner_pw,
            output=self.temp.name,
            bit128=True,
            suffix="128bit",
            algorithm=Algorithms.RC4_128
        )
        encrypted.encrypt()

        security = self._getPdfSecurity(encrypted)

        self.assertPdfExists(encrypted)
        self.assertEncrypted(encrypted)
        self.assert128BitEncryption(security, 3)
        self.assertSecurityValue(security, 4)
        self.assertPermissions(encrypted, can_print=True)

        expected_equals_output(function_name_to_file_name(), encrypted.output)

    @Timer.decorator
    def test_encrypt_40bit(self):
        encrypted = Encrypt(
            self.pdf_path,
            self.user_pw,
            self.owner_pw,
            output=self.temp.name,
            bit128=False,
            suffix="40bit",
            algorithm=Algorithms.RC4_40
        )
        encrypted.encrypt()

        security = self._getPdfSecurity(encrypted)

        self.assertPdfExists(encrypted)
        self.assertEncrypted(encrypted)
        self.assert40BitEncryption(security)
        self.assertSecurityValue(security, 4)
        self.assertPermissions(encrypted, can_print=True)

        expected_equals_output(function_name_to_file_name(), encrypted.output)

    @Timer.decorator
    def test_encrypt_128bit_allow_printing(self):
        # todo: allow and don't allow tests
        encrypted = Encrypt(
            self.pdf_path,
            self.user_pw,
            self.owner_pw,
            allow_printing=True,
            bit128=True,
            output=self.temp.name,
            suffix="128bit_allow_printing",
            algorithm=Algorithms.RC4_128
        )
        encrypted.encrypt()

        security = self._getPdfSecurity(encrypted)

        self.assertPdfExists(encrypted)
        self.assertEncrypted(encrypted)
        self.assert128BitEncryption(security, 3)
        self.assertSecurityValue(security, 4)
        self.assertPermissions(encrypted, can_print=True)

        expected_equals_output(function_name_to_file_name(), encrypted.output)

    @Timer.decorator
    def test_encrypt_128bit_allow_commenting(self):
        encrypted = Encrypt(
            self.pdf_path,
            self.user_pw,
            self.owner_pw,
            output=self.temp.name,
            allow_printing=False,
            allow_commenting=True,
            bit128=True,
            suffix="128bit_allow_commenting",
            algorithm=Algorithms.RC4_128
        )
        encrypted.encrypt()

        security = self._getPdfSecurity(encrypted)

        self.assertPdfExists(encrypted)
        self.assertEncrypted(encrypted)
        self.assertSecurityValue(security, 8)
        self.assertPermissions(encrypted, can_print=False, can_modify=True)

        expected_equals_output(function_name_to_file_name(), encrypted.output)

    @Timer.decorator
    def test_encrypt_128bit_allow_printing_and_commenting(self):
        encrypted = Encrypt(
            self.pdf_path,
            self.user_pw,
            self.owner_pw,
            output=self.temp.name,
            allow_printing=True,
            allow_commenting=True,
            bit128=True,
            suffix="128bit_allow_printing_and_commenting",
            algorithm=Algorithms.RC4_128
        )
        encrypted.encrypt()

        security = self._getPdfSecurity(encrypted)

        self.assertPdfExists(encrypted)
        self.assertEncrypted(encrypted)
        self.assert128BitEncryption(security, 3)
        self.assertSecurityValue(security, 12)
        self.assertPermissions(encrypted, can_print=True, can_modify=True)

        expected_equals_output(function_name_to_file_name(), encrypted.output)

    @Timer.decorator
    def test_encrypt_40bit_allow_printing(self):
        encrypted = Encrypt(
            self.pdf_path,
            self.user_pw,
            self.owner_pw,
            allow_printing=True,
            bit128=False,
            output=self.temp.name,
            suffix="40bit_allow_printing",
            algorithm=Algorithms.RC4_40
        )
        encrypted.encrypt()

        security = self._getPdfSecurity(encrypted)

        self.assertPdfExists(encrypted)
        self.assertEncrypted(encrypted)
        self.assert40BitEncryption(security)
        self.assertSecurityValue(security, 4)
        self.assertPermissions(encrypted, can_print=True)

        expected_equals_output(function_name_to_file_name(), encrypted.output)

    @Timer.decorator
    def test_encrypt_40bit_allow_commenting(self):
        encrypted = Encrypt(
            self.pdf_path,
            self.user_pw,
            self.owner_pw,
            output=self.temp.name,
            allow_printing=False,
            allow_commenting=True,
            bit128=False,
            suffix="40bit_allow_commenting",
            algorithm=Algorithms.RC4_40
        )
        encrypted.encrypt()

        security = self._getPdfSecurity(encrypted)

        self.assertPdfExists(encrypted)
        self.assertEncrypted(encrypted)
        self.assert40BitEncryption(security)
        self.assertSecurityValue(security, 8)
        self.assertPermissions(encrypted, can_print=False, can_modify=True)

        expected_equals_output(function_name_to_file_name(), encrypted.output)

    @Timer.decorator
    def test_encrypt_40bit_allow_printing_and_commenting(self):
        encrypted = Encrypt(
            self.pdf_path,
            self.user_pw,
            self.owner_pw,
            output=self.temp.name,
            allow_printing=True,
            allow_commenting=True,
            bit128=False,
            suffix="40bit_allow_printing_and_commenting",
            algorithm=Algorithms.RC4_40
        )
        encrypted.encrypt()

        security = self._getPdfSecurity(encrypted)

        self.assertPdfExists(encrypted)
        self.assertEncrypted(encrypted)
        self.assert40BitEncryption(security)
        self.assertSecurityValue(security, 12)
        self.assertPermissions(encrypted, can_print=True, can_modify=True)

        expected_equals_output(function_name_to_file_name(), encrypted.output)

    @Timer.decorator
    def test_encrypt_rc4_40(self):
        encrypted = Encrypt(
            self.pdf_path,
            self.user_pw,
            self.owner_pw,
            output=self.temp.name,
            suffix="rc4_40",
            algorithm=Algorithms.RC4_40
        )
        encrypted.encrypt()

        security = self._getPdfSecurity(encrypted)

        self.assertPdfExists(encrypted)
        self.assertEncrypted(encrypted)
        self.assert40BitEncryption(security)
        self.assertSecurityValue(security, 4)

        expected_equals_output(function_name_to_file_name(), encrypted.output)
        copy_pdf_to_output_directory(encrypted.output, function_name_to_file_name())

    @Timer.decorator
    def test_encrypt_rc4_128(self):
        encrypted = Encrypt(
            self.pdf_path,
            self.user_pw,
            self.owner_pw,
            output=self.temp.name,
            suffix="rc4_128",
            algorithm=Algorithms.RC4_128
        )
        encrypted.encrypt()

        security = self._getPdfSecurity(encrypted)

        self.assertPdfExists(encrypted)
        self.assertEncrypted(encrypted)
        self.assert128BitEncryption(security, 3)
        self.assertSecurityValue(security, 4)

        expected_equals_output(function_name_to_file_name(), encrypted.output)

    @Timer.decorator
    def test_encrypt_aes_128(self):
        encrypted = Encrypt(
            self.pdf_path,
            self.user_pw,
            self.owner_pw,
            output=self.temp.name,
            suffix="aes_128",
            algorithm=Algorithms.AES_128
        )
        encrypted.encrypt()

        security = self._getPdfSecurity(encrypted)

        self.assertPdfExists(encrypted)
        self.assertEncrypted(encrypted)
        self.assert128BitEncryption(security)
        self.assertSecurityValue(security, 4)

        expected_equals_output(function_name_to_file_name(), encrypted.output)

    @Timer.decorator
    def test_encrypt_aes_256_r5(self):
        encrypted = Encrypt(
            self.pdf_path,
            self.user_pw,
            self.owner_pw,
            output=self.temp.name,
            suffix="aes_256_45",
            algorithm=Algorithms.AES_256_r5
        )
        encrypted.encrypt()

        security = self._getPdfSecurity(encrypted)

        self.assertPdfExists(encrypted)
        self.assertEncrypted(encrypted)
        self.assert256BitEncryption(security)
        self.assertSecurityValue(security, 4)

        expected_equals_output(function_name_to_file_name(), encrypted.output)

    @Timer.decorator
    def test_encrypt_aes_256(self):
        encrypted = Encrypt(
            self.pdf_path,
            self.user_pw,
            self.owner_pw,
            output=self.temp.name,
            suffix="aes_256_45",
            algorithm=Algorithms.AES_256
        )
        encrypted.encrypt()

        security = self._getPdfSecurity(encrypted)

        self.assertPdfExists(encrypted)
        self.assertEncrypted(encrypted)
        self.assert256BitEncryption(security, 6)
        self.assertSecurityValue(security, 4)

        expected_equals_output(function_name_to_file_name(), encrypted.output)

    @Timer.decorator
    def test_password_byte_string(self):
        encrypted = Encrypt(
            self.pdf_path,
            self.user_pw,
            self.owner_pw,
            output=self.temp.name,
            suffix="byte_string",
            algorithm=Algorithms.RC4_128
        )
        encrypted.encrypt()

        security = self._getPdfSecurity(encrypted)

        self.assertPdfExists(encrypted)
        self.assertEncrypted(encrypted)
        self.assert128BitEncryption(security, 3)
        self.assertSecurityValue(security, 4)

        self.assertPermissions(encrypted, can_print=True)

        # Assert user & owner password byte string is correct
        self.assertEqual(
            security["/O"],
            "ÐHÑRžS]˘—Í8V6{˘KJ’ß\x01æ7ÑnÊ\x06[¯Nd’\x0b",
        )

        expected_equals_output(function_name_to_file_name(), encrypted.output)

    @Timer.decorator
    def test_encrypted_pdf_has_metadata(self):
        encrypted = Encrypt(
            self.pdf_path,
            self.user_pw,
            self.owner_pw,
            output=self.temp.name,
            bit128=True,
            suffix="metadata",
        )
        encrypted.encrypt()

        self.assertPdfExists(encrypted)
        self.assertEncrypted(encrypted)

        metadata = Info(encrypted.output, self.user_pw).metadata
        self.assertEqual(metadata["/Producer"], "pdfconduit")
        self.assertEqual(metadata["/Creator"], "pdfconduit")
        self.assertEqual(metadata["/Author"], "Stephen Neal")

        expected_equals_output(function_name_to_file_name(), encrypted.output)

    def _getPdfSecurity(self, encrypted):
        return Info(encrypted.output, self.user_pw).security

    def assertPdfExists(self, encrypted):
        # Assert that pdf file exists
        self.assertTrue(os.path.exists(encrypted.output))

    def assertEncrypted(self, pdf):
        self.assertTrue(Info(pdf.output, self.user_pw).encrypted)

    def assert128BitEncryption(self, security, security_handler_revision: int = 4):
        self.assertTrue("/Length" in security)
        self.assertIsInstance(security["/Length"], int)
        self.assertEqual(security["/Length"], 128)

        self.assertEqual(security["/Filter"], "/Standard")

        # Assert standard security handler revision is 3
        self.assertEqual(security["/R"], security_handler_revision)

        if security_handler_revision == 4:
            self.assertTrue('/CF' in security)
            self.assertEqual(security['/CF']['/StdCF']['/CFM'], '/AESV2')
        else:
            self.assertFalse('/CF' in security)

    def assert40BitEncryption(self, security):
        if "/Length" in security:
            self.assertEqual(security["/Length"], 40)

        # Assert standard security handler revision is 2
        self.assertEqual(security["/R"], 2)

    def assert256BitEncryption(self, security, security_handler_revision: int = 5):
        self.assertTrue("/Length" in security)
        self.assertIsInstance(security["/Length"], int)
        self.assertEqual(security["/Length"], 256)

        self.assertEqual(security["/Filter"], "/Standard")

        # Assert standard security handler revision is 3
        self.assertEqual(security["/R"], security_handler_revision)
        self.assertEqual(security["/V"], 5)

        self.assertTrue('/CF' in security)
        self.assertEqual(security['/CF']['/StdCF']['/CFM'], '/AESV3')

    def assertSecurityValue(self, security, expected):
        self.assertTrue("/P" in security)
        self.assertEqual(security["/P"], expected)

    def assertPermissions(
        self,
        pdf,
        can_print=False,
        can_modify=False,
        can_copy=False,
        can_annotate=False,
        can_fill_forms=False,
        can_change_accessability=False,
        can_assemble=False,
        can_print_high_quality=False,
    ):
        permissions = Info(pdf.output, self.user_pw).permissions
        self.assertEqual(permissions.can_print(), can_print)
        self.assertEqual(permissions.can_modify(), can_modify)
        self.assertEqual(permissions.can_copy(), can_copy)
        self.assertEqual(permissions.can_annotate(), can_annotate)
        self.assertEqual(permissions.can_fill_forms(), can_fill_forms)
        self.assertEqual(
            permissions.can_change_accessability(), can_change_accessability
        )
        self.assertEqual(permissions.can_assemble(), can_assemble)
        self.assertEqual(permissions.can_print_high_quality(), can_print_high_quality)


if __name__ == "__main__":
    unittest.main()
