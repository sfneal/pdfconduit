from typing import List

from parameterized import parameterized

from pdfconduit import Info, Pdfconduit
from tests import PdfconduitTestCase, get_clean_pdf_name, test_data_path


def decrypt_params() -> List[str]:
    return list(
        map(
            lambda filename: test_data_path(filename),
            [
                "article_encrypted.pdf",
                "manual_encrypted.pdf",
                "workbook_encrypted.pdf",
            ],
        )
    )


def decrypt_name_func(testcase_func, param_num, param):
    return "{}.{}".format(
        testcase_func.__name__,
        get_clean_pdf_name(param.args[0]),
    )


class TestDecrypt(PdfconduitTestCase):
    @parameterized.expand(decrypt_params, name_func=decrypt_name_func)
    def test_can_decrypt(self, path: str):
        self.assertTrue(Info(path).encrypted)
        self.conduit = (
            Pdfconduit(path, "foo")
            .set_output_directory(self.temp.name)
            .set_output_suffix("decrypted")
        )
        self.conduit.write()

        self.assertPdfExists(self.conduit.output)
        self.assertFalse(self.conduit.info.encrypted)
        self.assertTrue(self.conduit.info.decrypted)

        # Double check
        self.assertFalse(Info(self.conduit.output).encrypted)
        self.assertTrue(Info(self.conduit.output).decrypted)
