import os
import unittest
from tempfile import TemporaryDirectory
from typing import List, Tuple

from parameterized import parameterized

from pdfconduit import Info, Rotate
from pdfconduit.utils.driver import Driver
from tests import *


def can_rotate_params() -> List[Tuple[str, Driver, int]]:
    return [
        ('pdfrw_90', Driver.pdfrw, 90),
        ('pdfrw_180', Driver.pdfrw, 180),
        ('pdfrw_270', Driver.pdfrw, 270),
        ('pypdf_90', Driver.pypdf, 90),
        ('pypdf_180', Driver.pypdf, 180),
        ('pypdf_270', Driver.pypdf, 270),
    ]


def cannot_rotate_params() -> List[Tuple[str, Driver, int]]:
    return [
        ('pypdf_135', Driver.pypdf, 135),
        ('pypdf_225', Driver.pypdf, 225),
        ('pypdf_315', Driver.pypdf, 315),
    ]


class TestRotate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdf_path = pdf_path

    def setUp(self):
        self.temp = TemporaryDirectory()

    def tearDown(self):
        self.temp.cleanup()

    @parameterized.expand(can_rotate_params)
    def test_can_rotate(self, name: str, driver: Driver, rotation: int):
        rotated = (
            Rotate(
                self.pdf_path,
                rotation,
                suffix="rotated_{}_{}".format(driver.name, rotation),
                tempdir=self.temp.name,
            )
            .use(driver)
            .rotate()
        )

        self.assertPdfExists(rotated)
        self.assertPdfRotation(rotated, rotation)

    @parameterized.expand(cannot_rotate_params)
    def test_can_only_rotate_by_90_using_pypdf(self, name: str, driver: Driver, rotation: int):
        with self.assertRaises(ValueError) as context:
            rotated = (
                Rotate(
                    self.pdf_path,
                    rotation,
                    suffix="rotated_{}_{}".format(driver.name, rotation),
                    tempdir=self.temp.name,
                )
                .use(driver)
                .rotate()
            )

        self.assertTrue("Rotation angle must be a multiple of 90" in str(context.exception))

    def assertPdfExists(self, pdf):
        self.assertTrue(os.path.isfile(pdf))

    def assertPdfDoesntExists(self, pdf):
        self.assertFalse(os.path.isfile(pdf))

    def assertPdfRotation(self, rotated, rotation):
        self.assertEqual(Info(rotated).rotate, rotation)


if __name__ == "__main__":
    unittest.main()
