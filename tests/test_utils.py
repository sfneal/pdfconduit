import os
from typing import Tuple, List, Optional

from parameterized import parameterized

from pdfconduit import Info, Pdfconduit
from pdfconduit.utils import add_suffix
from tests import PdfconduitTestCase, get_clean_pdf_name
from tests import test_data_path


def unencrypted_pdf_params() -> List[str]:
    return list(
        map(
            lambda filename: test_data_path(filename),
            ["article.pdf", "manual.pdf", "workbook.pdf"],
        )
    )


def encrypted_pdf_params() -> List[str]:
    return list(
        map(
            lambda filepath: add_suffix(filepath, "encrypted"), unencrypted_pdf_params()
        )
    )


def pages_params() -> List[Tuple[str, int]]:
    return [
        (test_data_path("article.pdf"), 1),
        (test_data_path("manual.pdf"), 82),
        (test_data_path("workbook.pdf"), 128),
    ]


def dimensions_params() -> List[Tuple[str, float, float]]:
    default_w = 595.276
    default_h = 841.89
    return [
        (test_data_path("article.pdf"), default_w, default_h),
        (test_data_path("manual.pdf"), default_w, default_h),
        (test_data_path("workbook.pdf"), default_w, default_h),
        (test_data_path("con docs.pdf"), 2592.0, 1728.0),
    ]


def info_name_func(testcase_func, param_num, param):
    return "{}.{}".format(
        testcase_func.__name__, get_clean_pdf_name(param.args[0]).replace(" ", "_")
    )


class TestInfo(PdfconduitTestCase):
    @parameterized.expand(encrypted_pdf_params, name_func=info_name_func)
    def test_is_encrypted(self, filepath: str):
        info = self._get_info(filepath)
        self.assertTrue(info.encrypted)

    @parameterized.expand(unencrypted_pdf_params, name_func=info_name_func)
    def test_is_decrypted(self, filepath: str):
        info = self._get_info(filepath)
        self.assertTrue(info.decrypted)

    @parameterized.expand(unencrypted_pdf_params, name_func=info_name_func)
    def test_is_not_encrypted(self, filepath: str):
        info = self._get_info(filepath)

        self.assertFalse(info.encrypted)

    @parameterized.expand(encrypted_pdf_params, name_func=info_name_func)
    def test_is_not_decrypted(self, filepath: str):
        info = self._get_info(filepath)
        self.assertFalse(info.decrypted)

    @parameterized.expand(pages_params, name_func=info_name_func)
    def test_pages(self, filepath: str, expected_pages: int):
        info = self._get_info(filepath)

        self.assertIsInstance(info.pages, int)
        self.assertEqual(info.pages, expected_pages)

    def test_metadata(self):
        info = self._get_info(test_data_path("article.pdf"))

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
        info = self._get_info(test_data_path("article.pdf"))

        self.assertEqual(info.pages, len(info.resources()))

        resources = info.resources()[0]
        self.assertIsInstance(resources, dict)
        self.assertEqual(resources["/Type"], "/Page")

        mediabox = list(resources["/MediaBox"])
        self.assertEqual(mediabox[0], 0)
        self.assertEqual(mediabox[1], 0)
        self.assertEqual(float(mediabox[2]), 595.276)
        self.assertEqual(float(mediabox[3]), 841.89)

    @parameterized.expand(encrypted_pdf_params, name_func=info_name_func)
    def test_security_encrypted_pdf(self, filepath: str):
        info = self._get_info(filepath)

        self.assertIsInstance(info.security, dict)
        self.assertTrue("/V" in info.security)
        self.assertTrue("/R" in info.security)
        self.assertTrue("/Length" in info.security)
        self.assertTrue("/P" in info.security)
        self.assertTrue("/Filter" in info.security)
        self.assertTrue("/O" in info.security)
        self.assertTrue("/U" in info.security)

    @parameterized.expand(encrypted_pdf_params, name_func=info_name_func)
    def test_security_decrypted_pdf(self, filepath: str):
        info = self._get_info(filepath, "baz")

        self.assertIsInstance(info.security, dict)
        self.assertTrue("/V" in info.security)
        self.assertTrue("/R" in info.security)
        self.assertTrue("/Length" in info.security)
        self.assertTrue("/P" in info.security)
        self.assertTrue("/Filter" in info.security)
        self.assertTrue("/O" in info.security)
        self.assertTrue("/U" in info.security)

    @parameterized.expand(unencrypted_pdf_params, name_func=info_name_func)
    def test_security_passwordless_pdf(self, filepath: str):
        info = self._get_info(filepath)

        self.assertIsInstance(info.security, dict)
        self.assertEqual(info.security, {})

    @parameterized.expand(dimensions_params, name_func=info_name_func)
    def test_dimensions(
        self, filepath: str, expected_width: float, expected_height: float
    ):
        info = self._get_info(filepath)

        self.assertIsInstance(info.dimensions, dict)
        self.assertTrue("w" in info.dimensions)
        self.assertTrue("h" in info.dimensions)
        self.assertIsInstance(info.dimensions["w"], float)
        self.assertIsInstance(info.dimensions["h"], float)
        self.assertEqual(info.dimensions["w"], expected_width)
        self.assertEqual(info.dimensions["h"], expected_height)

    @parameterized.expand(dimensions_params, name_func=info_name_func)
    def test_size(self, filepath: str, expected_width: float, expected_height: float):
        info = self._get_info(filepath)

        self.assertIsInstance(info.size, tuple)
        self.assertEqual(len(info.size), 2)
        self.assertIsInstance(info.size[0], float)
        self.assertIsInstance(info.size[1], float)
        self.assertEqual(info.size[0], expected_width)
        self.assertEqual(info.size[1], expected_height)

    @parameterized.expand(dimensions_params, name_func=info_name_func)
    def test_size_and_dimensions_are_equal(
        self, filepath: str, expected_width: float, expected_height: float
    ):
        info = self._get_info(filepath)
        self.assertEqual(info.size[0], info.dimensions["w"])
        self.assertEqual(info.size[1], info.dimensions["h"])

    @parameterized.expand(unencrypted_pdf_params, name_func=info_name_func)
    def test_rotate_no_rotation(self, filepath: str):
        info = self._get_info(filepath)
        self.assertEqual(info.rotate, None)

    def test_rotate_rotated(self):
        info = self._get_info(test_data_path("rotated.pdf"))

        self.assertIsInstance(info.rotate, int)
        self.assertEqual(info.rotate, 90)

    @parameterized.expand(unencrypted_pdf_params, name_func=info_name_func)
    def test_get_all_info_unencrypted(self, filepath: str):
        info = self._get_info(filepath)
        info_all = info.all

        self.assertIsInstance(info_all, dict)

    @parameterized.expand(encrypted_pdf_params, name_func=info_name_func)
    def test_get_all_info_encrypted(self, filepath: str):
        info = self._get_info(filepath, "baz")
        info_all = info.all

        self.assertIsInstance(info_all, dict)

    @parameterized.expand(unencrypted_pdf_params, name_func=info_name_func)
    def test_get_all_info_unencrypted_from_stream(self, filepath: str):
        conduit = Pdfconduit(self._get_pdf_byte_stream(filepath))
        info = conduit.info.all

        self.assertIsInstance(info, dict)

    @parameterized.expand(encrypted_pdf_params, name_func=info_name_func)
    def test_get_all_info_encrypted_from_stream(self, filepath: str):
        conduit = Pdfconduit(self._get_pdf_byte_stream(filepath), "baz")
        info = conduit.info.all

        self.assertIsInstance(info, dict)

    @staticmethod
    def _get_info(filepath: str, password: Optional[str] = None) -> Info:
        return Pdfconduit(filepath, password, with_writer=False).info


def get_expected_output(filepath: str, suffix: str = "modified", sep: str = "_") -> str:
    return os.path.join(
        os.path.dirname(filepath),
        os.path.basename(filepath).replace(".pdf", "") + sep + suffix + ".pdf",
    )


def path_params() -> List[Tuple[str, str, str]]:
    return [
        (get_expected_output(path, suffix), path, suffix)
        for path in unencrypted_pdf_params()
        for suffix in ["modified", "new", "old", "backup", "changed"]
    ]


def path_params_with_sep() -> List[Tuple[str, str, str, str]]:
    return [
        (get_expected_output(path, suffix, sep), path, suffix, sep)
        for path in unencrypted_pdf_params()
        for suffix in ["modified", "new", "old", "backup", "changed"]
        for sep in ["_", "-"]
    ]


def path_name_func(testcase_func, param_num, param):
    return "{}-{}".format(
        testcase_func.__name__, os.path.basename(str(param.args[0])).replace(" ", "_")
    )


class TestPath(PdfconduitTestCase):
    @parameterized.expand(path_params, name_func=info_name_func)
    def test_add_suffix(self, expected: str, filepath: str, suffix: str):
        with_suffix = add_suffix(filepath, suffix)

        self.assertIsInstance(with_suffix, str)
        self.assertEqual(with_suffix, expected)

    @parameterized.expand(path_params_with_sep, name_func=info_name_func)
    def test_add_suffix_suffix_sep(
        self, expected: str, filepath: str, suffix: str, sep: str
    ):
        with_suffix = add_suffix(filepath, suffix, sep)

        self.assertIsInstance(with_suffix, str)
        self.assertEqual(with_suffix, expected)

    @parameterized.expand(path_params_with_sep, name_func=info_name_func)
    def test_add_suffix_suffix_sep_ext(
        self, expected: str, filepath: str, suffix: str, sep: str
    ):
        with_suffix = add_suffix(filepath, suffix, sep, "zip")

        self.assertIsInstance(with_suffix, str)
        self.assertEqual(with_suffix, expected.replace(".pdf", ".zip"))
