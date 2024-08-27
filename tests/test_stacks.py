from parameterized import parameterized

from pdfconduit import Pdfconduit, Info
from pdfconduit.settings import Encryption
from pdfconduit.utils.typing import List, Iterable
from tests import *
from tests.test_encrypt import EncryptionTestCase
from tests.test_merge import merge_name_func


def stack_params() -> List[str]:
    return list(
        map(
            lambda filename: test_data_path(filename),
            [
                "article.pdf",
                "charts.pdf",
                "document.pdf",
                # "workbook.pdf",
            ],
        )
    )


def stack_name_func(testcase_func, param_num, param):
    return "{}.{}".format(
        testcase_func.__name__,
        get_clean_pdf_name(param.args[0]),
    )


def merge_params():
    params = [
        ("document.pdf", ["article.pdf", "charts.pdf"]),
        ("article.pdf", ["document.pdf"]),
        ("charts.pdf", ["article.pdf", "document.pdf"]),
    ]
    return [
        (test_data_path(main_pdf), list(map(lambda pdf: test_data_path(pdf), to_merge)))
        for main_pdf, to_merge in params
    ]


ENCRYPTOR = Encryption(user_pw="baz", owner_pw="foo")


class TestStacks(EncryptionTestCase):
    def createConduit(self, path: str, suffix: str):
        return (
            Pdfconduit(path)
            .set_output_directory(self.temp.name)
            .set_output_suffix(suffix)
        )

    def assertEncryption(self, conduit: Pdfconduit):
        security = self._getPdfSecurity(conduit)

        self.assertEncrypted(conduit)
        self.assert256BitEncryption(security, 5)
        self.assertPermissions(
            conduit,
            can_print=ENCRYPTOR.allow_printing,
            can_modify=ENCRYPTOR.allow_commenting,
        )

    @parameterized.expand(merge_params, name_func=merge_name_func)
    def test_can_merge_and_encrypt(self, path: str, pdfs_to_merge: Iterable[str]):
        self.conduit = self.createConduit(path, "merged_encrypted")
        for pdf in pdfs_to_merge:
            self.conduit.merge(pdf)

        self.assertCorrectNumPages(path, pdfs_to_merge, self.conduit.info.pages)

        self.conduit.encrypt(ENCRYPTOR)
        self.conduit.write()

        self.assertPdfExists(self.conduit.output)
        self.assertEncryption(self.conduit)

    @parameterized.expand(merge_params, name_func=merge_name_func)
    def test_can_merge_fast_and_encrypt(self, path: str, pdfs_to_merge: Iterable[str]):
        self.conduit = self.createConduit(path, "merged_fast_encrypted")
        self.conduit.merge_fast(list(pdfs_to_merge))

        self.assertCorrectNumPages(path, pdfs_to_merge, self.conduit.info.pages)

        self.conduit.encrypt(ENCRYPTOR)
        self.conduit.write()

        self.assertPdfExists(self.conduit.output)
        self.assertEncryption(self.conduit)

    @parameterized.expand(merge_params, name_func=merge_name_func)
    def test_can_merge_and_rotate(self, path: str, pdfs_to_merge: Iterable[str]):
        self.conduit = self.createConduit(path, "merged_rotated")
        for pdf in pdfs_to_merge:
            self.conduit.merge(pdf)
        self.conduit.rotate(90)
        self.conduit.write()

        self.assertPdfExists(self.conduit.output)
        self.assertCorrectNumPages(path, pdfs_to_merge, self.conduit.info.pages)
        self.assertPdfRotation(self.conduit, 90)

    @parameterized.expand(merge_params, name_func=merge_name_func)
    def test_can_merge_rotate_and_encrypt(
        self, path: str, pdfs_to_merge: Iterable[str]
    ):
        self.conduit = self.createConduit(path, "merged_rotated_encrypted")
        for pdf in pdfs_to_merge:
            self.conduit.merge(pdf)

        self.assertCorrectNumPages(path, pdfs_to_merge, self.conduit.info.pages)

        self.conduit.rotate(90)

        self.assertPdfRotation(self.conduit, 90)

        self.conduit.encrypt(ENCRYPTOR)
        self.conduit.write()

        self.assertPdfExists(self.conduit.output)
        self.assertEncryption(self.conduit)

    @parameterized.expand(stack_params, name_func=stack_name_func)
    def test_can_rotate_and_encrypt(self, path: str):
        self.conduit = self.createConduit(path, "rotated_encrypted")
        self.conduit.rotate(90)

        self.assertPdfRotation(self.conduit, 90)

        self.conduit.encrypt(ENCRYPTOR)
        self.conduit.write()

        self.assertPdfExists(self.conduit.output)
        self.assertEncryption(self.conduit)

    @parameterized.expand(merge_params, name_func=merge_name_func)
    def test_can_merge_and_slice(self, path: str, pdfs_to_merge: Iterable[str]):
        self.conduit = self.createConduit(path, "merged_sliced")
        for pdf in pdfs_to_merge:
            self.conduit.merge(pdf)
        self.conduit.slice(2, 5)
        self.conduit.write()

        self.assertPdfExists(self.conduit.output)
        self.assertCorrectPagesSliced(2, 5, self.conduit)

    @parameterized.expand(merge_params, name_func=merge_name_func)
    def test_can_merge_slice_and_encrypt(self, path: str, pdfs_to_merge: Iterable[str]):
        self.conduit = self.createConduit(path, "merged_sliced_encrypted")
        for pdf in pdfs_to_merge:
            self.conduit.merge(pdf)

        self.assertCorrectNumPages(path, pdfs_to_merge, self.conduit.info.pages)

        self.conduit.slice(2, 5)

        self.assertCorrectPagesSliced(2, 5, self.conduit)

        self.conduit.encrypt(ENCRYPTOR)
        self.conduit.write()

        self.assertPdfExists(self.conduit.output)
        self.assertEncryption(self.conduit)

    @parameterized.expand(merge_params, name_func=merge_name_func)
    def test_can_merge_and_scale(self, path: str, pdfs_to_merge: Iterable[str]):
        self.conduit = self.createConduit(path, "merged_scaled")
        for pdf in pdfs_to_merge:
            self.conduit.merge(pdf)
        self.conduit.scale(2.0)
        self.conduit.write()

        self.assertPdfExists(self.conduit.output)
        self.assertCorrectNumPages(path, pdfs_to_merge, self.conduit.info.pages)
        self.assertPdfScaled(2.0, self.conduit, path)

    @parameterized.expand(merge_params, name_func=merge_name_func)
    def test_can_merge_scale_and_encrypt(self, path: str, pdfs_to_merge: Iterable[str]):
        self.conduit = self.createConduit(path, "merged_scaled_encrypted")
        for pdf in pdfs_to_merge:
            self.conduit.merge(pdf)

        self.assertCorrectNumPages(path, pdfs_to_merge, self.conduit.info.pages)

        self.conduit.scale(2.0)

        self.assertPdfScaled(2.0, self.conduit, path)

        self.conduit.encrypt(ENCRYPTOR)
        self.conduit.write()

        self.assertPdfExists(self.conduit.output)
        self.assertEncryption(self.conduit)

    @parameterized.expand(stack_params, name_func=stack_name_func)
    def test_can_scale_and_flatten(self, path: str):
        self.conduit = self.createConduit(path, "scaled_flattened")
        self.conduit.scale(2.0)
        self.conduit.flatten()

        self.assertPdfExists(self.conduit.output)
        self.assertPdfScaled(2.0, self.conduit, path)
        self.assertPdfPagesEqual(path, self.conduit.output)

    @parameterized.expand(merge_params, name_func=merge_name_func)
    def test_can_merge_and_flatten(self, path: str, pdfs_to_merge: Iterable[str]):
        self.conduit = self.createConduit(path, "merged_flattened")
        for pdf in pdfs_to_merge:
            self.conduit.merge(pdf)
        self.conduit.flatten()

        self.assertPdfExists(self.conduit.output)
        self.assertCorrectNumPages(path, pdfs_to_merge, self.conduit.info.pages)

    @parameterized.expand(merge_params, name_func=merge_name_func)
    def test_can_merge_and_remove_duplication(
        self, path: str, pdfs_to_merge: Iterable[str]
    ):
        self.conduit = self.createConduit(path, "merged_noimages")
        for pdf in pdfs_to_merge:
            self.conduit.merge(pdf)
        self.conduit.remove_images()
        self.conduit.write()

        self.assertPdfExists(self.conduit.output)
        self.assertEqual(0, self.conduit.info.images_count)

        self.assertCorrectNumPages(path, pdfs_to_merge, self.conduit.info.pages)

    @parameterized.expand(stack_params, name_func=stack_name_func)
    def test_can_scale_and_compress(self, path: str):
        self.conduit = self.createConduit(path, "scaled_compressed")
        self.conduit.scale(2.0)
        self.conduit.compress()
        self.conduit.write()

        self.assertPdfExists(self.conduit.output)
        self.assertPdfScaled(2.0, self.conduit, path)
        self.assertEqual(Info(path).images_count, self.conduit.info.images_count)

    @parameterized.expand(stack_params, name_func=stack_name_func)
    def test_can_scale_and_reduce_image_quality(self, path: str):
        self.conduit = self.createConduit(path, "scaled_reduced_image_quality")
        self.conduit.scale(2.0)
        self.conduit.reduce_image_quality(50)
        self.conduit.write()

        self.assertPdfExists(self.conduit.output)
        self.assertEqual(Info(path).images_count, self.conduit.info.images_count)
        if path.endswith("document.pdf"):
            print("Skipping document.pdf because it yields the same size")
            return
        self.assertFileSizeDecreased(
            self.createConduit(path, "scaled").scale(2.0).write(), self.conduit.output
        )

    @parameterized.expand(merge_params, name_func=merge_name_func)
    def test_can_merge_scale_flatten_and_encrypt(
        self, path: str, pdfs_to_merge: Iterable[str]
    ):
        self.conduit = self.createConduit(path, "merged_scaled_flattened_encrypted")
        for pdf in pdfs_to_merge:
            self.conduit.merge(pdf)

        self.assertCorrectNumPages(path, pdfs_to_merge, self.conduit.info.pages)

        self.conduit.scale(2.0)

        self.assertPdfScaled(2.0, self.conduit, path)

        self.conduit.flatten()

        self.assertPdfExists(self.conduit.output)
        self.assertCorrectNumPages(path, pdfs_to_merge, self.conduit.info.pages)

        self.conduit.encrypt(ENCRYPTOR)
        self.conduit.write()

        self.assertPdfExists(self.conduit.output)
        self.assertEncryption(self.conduit)
