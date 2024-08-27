from typing import List, Tuple

from parameterized import parameterized

from pdfconduit import Info
from pdfconduit.settings import Algorithms, Encryption
from tests import PdfconduitTestCase


def encryption_name_func(testcase_func, param_num, param):
    name = ""
    if not param.args[0].allow_printing and not param.args[0].allow_commenting:
        name += "_none"
    if param.args[0].allow_printing:
        name += "_printing"
    if param.args[0].allow_commenting:
        name += "_commenting"
    return "{}.{}.{}".format(testcase_func.__name__, param.args[0].algo.value, name[1:])


def encryption_params() -> List[Tuple[Encryption, int]]:
    algos = [
        # (name, algo, expected_security_handler)
        (Algorithms.RC4_40, 2),
        (Algorithms.RC4_128, 3),
        (Algorithms.AES_128, 4),
        (Algorithms.AES_256, 6),
        (Algorithms.AES_256_r5, 5),
    ]

    permissions = [
        {"allow_printing": True, "allow_commenting": False},
        {"allow_printing": True, "allow_commenting": True},
        {"allow_printing": False, "allow_commenting": True},
        {"allow_printing": False, "allow_commenting": False},
    ]

    params = []
    for algo in algos:
        algorithm, expected_security_handler = algo
        for permission in permissions:
            params.append(
                (
                    Encryption(
                        user_pw="baz",
                        owner_pw="foo",
                        allow_printing=permission["allow_printing"],
                        allow_commenting=permission["allow_commenting"],
                        algo=algorithm,
                    ),
                    expected_security_handler,
                )
            )
    return params


class EncryptionTestCase(PdfconduitTestCase):
    def _getPdfSecurity(self, encrypted):
        return Info(encrypted.output, self.user_pw).security

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


class TestEncryption(EncryptionTestCase):
    @parameterized.expand(encryption_params, name_func=encryption_name_func)
    def test_can_encrypt_pdf(
        self, encryption: Encryption, expected_security_handler: int
    ):
        self.conduit.encrypt(encryption).write()

        security = self._getPdfSecurity(self.conduit)

        self.assertPdfExists(self.conduit.output)
        self.assertEncrypted(self.conduit)
        if encryption.algo.bit_length == 40:
            self.assert40BitEncryption(security)
        if encryption.algo.bit_length == 128:
            self.assert128BitEncryption(security, expected_security_handler)
        if encryption.algo.bit_length == 256:
            self.assert256BitEncryption(security, expected_security_handler)

        # self.assertSecurityValue(security, 4)
        self.assertPermissions(
            self.conduit,
            can_print=encryption.allow_printing,
            can_modify=encryption.allow_commenting,
        )

    def test_password_byte_string(self):
        self.conduit.encrypt(
            Encryption(user_pw="baz", owner_pw="foo", algo=Algorithms.RC4_128)
        ).write()

        security = self._getPdfSecurity(self.conduit)

        self.assertPdfExists(self.conduit.output)
        self.assertEncrypted(self.conduit)
        self.assert128BitEncryption(security, 3)
        self.assertSecurityValue(security, 4)

        self.assertPermissions(self.conduit, can_print=True)

        # Assert user & owner password byte string is correct
        self.assertEqual(
            security["/O"],
            "ÐHÑRžS]˘—Í8V6{˘KJ’ß\x01æ7ÑnÊ\x06[¯Nd’\x0b",
        )
