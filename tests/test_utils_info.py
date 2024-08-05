import unittest

from pdfconduit import Info
from tests import *


class TestInfo(unittest.TestCase):

    def test_is_encrypted(self):
        info = self._get_info("encrypted.pdf")

        self.assertTrue(info.encrypted)

    def test_is_decrypted(self):
        info = self._get_info("article.pdf")

        self.assertTrue(info.decrypted)

    def test_is_not_encrypted(self):
        info = self._get_info("article.pdf")

        self.assertFalse(info.encrypted)

    def test_is_not_decrypted(self):
        info = self._get_info("encrypted.pdf")

        self.assertFalse(info.decrypted)

    def test_pages(self):
        info = self._get_info("article.pdf")

        self.assertIsInstance(info.pages, int)
        self.assertEqual(info.pages, 1)
        self.assertEqual(Info(test_data_path("document.pdf")).pages, 11)

    def test_metadata(self):
        info = self._get_info("article.pdf")

        self.assertIsInstance(info.metadata, dict)
        self.assertEqual(
            info.metadata["/Creator"], "This PDF is created by PDF4U Pro 2.0"
        )
        self.assertEqual(
            info.metadata["/CreationDate"],
            "D:20040120105826",
        )
        self.assertEqual(
            info.metadata["/Producer"],
            "PDF4U Adobe PDF Creator 2.0",
        )

    def test_resources(self):
        info = self._get_info("article.pdf")

        self.assertEqual(info.pages, len(info.resources()))

        resources = info.resources()[0]
        self.assertIsInstance(resources, dict)
        self.assertEqual(resources["/Type"], "/Page")

        mediabox = list(resources["/MediaBox"])
        self.assertEqual(mediabox[0], 0)
        self.assertEqual(mediabox[1], 0)
        self.assertEqual(float(mediabox[2]), 595.276)
        self.assertEqual(float(mediabox[3]), 841.89)

    def test_security_encrypted_pdf(self):
        info = self._get_info("encrypted.pdf")

        self.assertIsInstance(info.security, dict)
        self.assertTrue("/V" in info.security)
        self.assertTrue("/R" in info.security)
        self.assertTrue("/Length" in info.security)
        self.assertTrue("/P" in info.security)
        self.assertTrue("/Filter" in info.security)
        self.assertTrue("/O" in info.security)
        self.assertTrue("/U" in info.security)

    def test_security_decrypted_pdf(self):
        info = self._get_info("encrypted.pdf", "foo")

        self.assertIsInstance(info.security, dict)
        self.assertTrue("/V" in info.security)
        self.assertTrue("/R" in info.security)
        self.assertTrue("/Length" in info.security)
        self.assertTrue("/P" in info.security)
        self.assertTrue("/Filter" in info.security)
        self.assertTrue("/O" in info.security)
        self.assertTrue("/U" in info.security)

    def test_security_passwordless_pdf(self):
        info = self._get_info("article.pdf")

        self.assertIsInstance(info.security, dict)
        self.assertEqual(info.security, {})

    def test_dimensions(self):
        info = self._get_info("article.pdf")

        self.assertIsInstance(info.dimensions, dict)
        self.assertTrue("w" in info.dimensions)
        self.assertTrue("h" in info.dimensions)
        self.assertIsInstance(info.dimensions["w"], float)
        self.assertIsInstance(info.dimensions["h"], float)
        self.assertEqual(info.dimensions["w"], 595.276)
        self.assertEqual(info.dimensions["h"], 841.89)

    def test_size(self):
        info = self._get_info("article.pdf")

        self.assertIsInstance(info.size, tuple)
        self.assertEqual(len(info.size), 2)
        self.assertIsInstance(info.size[0], float)
        self.assertIsInstance(info.size[1], float)
        self.assertEqual(info.size[0], 595.276)
        self.assertEqual(info.size[1], 841.89)

    def test_size_and_dimensions_are_equal(self):
        info = self._get_info("article.pdf")

        self.assertEqual(info.size[0], info.dimensions["w"])
        self.assertEqual(info.size[1], info.dimensions["h"])

    def test_rotate_no_rotation(self):
        info = self._get_info("article.pdf")

        self.assertEqual(info.rotate, None)

    def test_rotate_rotated(self):
        info = self._get_info("rotated.pdf")

        self.assertIsInstance(info.rotate, int)
        self.assertEqual(info.rotate, 90)

    @staticmethod
    def _get_info(filename, password=None):
        return Info(test_data_path(filename), password=password)


if __name__ == "__main__":
    unittest.main()
