import os
import unittest
from tempfile import NamedTemporaryFile
from typing import List, Tuple

from parameterized import parameterized

from pdfconduit.conduit import Encrypt
from pdfconduit.conduit.encrypt import Algorithms
from pdfconduit.utils import Info
from tests import *


def encryption_algo_params() -> List[Tuple[str, Algorithms, int]]:
    return [
        ("RC4-40", Algorithms.RC4_40, 2),
        ("RC4-128", Algorithms.RC4_128, 3),
        ("AES-128", Algorithms.AES_128, 4),
        ("AES-256", Algorithms.AES_256, 6),
        ("AES-256-R5", Algorithms.AES_256_r5, 5),
    ]


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

    @parameterized.expand(encryption_algo_params)
    def test_encryption_algorithms(
        self, name: str, algorithm: Algorithms, expected_security_handler: int
    ):
        encrypted = Encrypt(
            self.pdf_path,
            self.user_pw,
            self.owner_pw,
            output=self.temp.name,
            bit128=algorithm.is_128bit,
            suffix=algorithm.name,
            algorithm=algorithm,
        )
        encrypted.encrypt()

        security = self._getPdfSecurity(encrypted)

        self.assertPdfExists(encrypted)
        self.assertEncrypted(encrypted)
        if algorithm.bit_length == 40:
            self.assert40BitEncryption(security)
        if algorithm.bit_length == 128:
            self.assert128BitEncryption(security, expected_security_handler)
        if algorithm.bit_length == 256:
            self.assert256BitEncryption(security, expected_security_handler)

        self.assertSecurityValue(security, 4)
        self.assertPermissions(encrypted, can_print=True)

    @parameterized.expand(encryption_algo_params)
    def test_permission_can_print(
        self, name: str, algorithm: Algorithms, expected_security_handler: int
    ):
        encrypted = Encrypt(
            self.pdf_path,
            self.user_pw,
            self.owner_pw,
            output=self.temp.name,
            bit128=algorithm.is_128bit,
            suffix=algorithm.name,
            algorithm=algorithm,
            allow_printing=True,
            allow_commenting=False,
        )
        encrypted.encrypt()

        self.assertPdfExists(encrypted)
        self.assertEncrypted(encrypted)

        self.assertPermissions(encrypted, can_print=True, can_modify=False)

    @parameterized.expand(encryption_algo_params)
    def test_permission_can_comment(
        self, name: str, algorithm: Algorithms, expected_security_handler: int
    ):
        encrypted = Encrypt(
            self.pdf_path,
            self.user_pw,
            self.owner_pw,
            output=self.temp.name,
            bit128=algorithm.is_128bit,
            suffix=algorithm.name,
            algorithm=algorithm,
            allow_printing=False,
            allow_commenting=True,
        )
        encrypted.encrypt()

        self.assertPdfExists(encrypted)
        self.assertEncrypted(encrypted)

        self.assertPermissions(encrypted, can_print=False, can_modify=True)

    @parameterized.expand(encryption_algo_params)
    def test_permission_can_print_and_comment(
        self, name: str, algorithm: Algorithms, expected_security_handler: int
    ):
        encrypted = Encrypt(
            self.pdf_path,
            self.user_pw,
            self.owner_pw,
            output=self.temp.name,
            bit128=algorithm.is_128bit,
            suffix=algorithm.name,
            algorithm=algorithm,
            allow_printing=True,
            allow_commenting=True,
        )
        encrypted.encrypt()

        self.assertPdfExists(encrypted)
        self.assertEncrypted(encrypted)

        self.assertPermissions(encrypted, can_print=True, can_modify=True)

    def test_password_byte_string(self):
        encrypted = Encrypt(
            self.pdf_path,
            self.user_pw,
            self.owner_pw,
            output=self.temp.name,
            suffix="byte_string",
            algorithm=Algorithms.RC4_128,
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

    def _getPdfSecurity(self, encrypted):
        return Info(encrypted.output, self.user_pw).security

    def assertPdfExists(self, encrypted):
        # Assert that pdf file exists
        self.assertTrue(os.path.exists(encrypted.output))

    def assertEncrypted(self, pdf):
        self.assertTrue(Info(pdf.output, self.user_pw).encrypted)

    def assert40BitEncryption(self, security):
        if "/Length" in security:
            self.assertEqual(security["/Length"], 40)

        # Assert standard security handler revision is 2
        self.assertEqual(security["/R"], 2)

    def assert128BitEncryption(self, security, security_handler_revision: int = 4):
        self.assertTrue("/Length" in security)
        self.assertIsInstance(security["/Length"], int)
        self.assertEqual(security["/Length"], 128)

        self.assertEqual(security["/Filter"], "/Standard")

        # Assert standard security handler revision is 3
        self.assertEqual(security["/R"], security_handler_revision)

        if security_handler_revision == 4:
            self.assertTrue("/CF" in security)
            self.assertEqual(security["/CF"]["/StdCF"]["/CFM"], "/AESV2")
        else:
            self.assertFalse("/CF" in security)

    def assert256BitEncryption(self, security, security_handler_revision: int = 5):
        self.assertTrue("/Length" in security)
        self.assertIsInstance(security["/Length"], int)
        self.assertEqual(security["/Length"], 256)

        self.assertEqual(security["/Filter"], "/Standard")

        # Assert standard security handler revision is 3
        self.assertEqual(security["/R"], security_handler_revision)
        self.assertEqual(security["/V"], 5)

        self.assertTrue("/CF" in security)
        self.assertEqual(security["/CF"]["/StdCF"]["/CFM"], "/AESV3")

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
