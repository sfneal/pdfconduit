import os
import unittest
from tempfile import TemporaryDirectory
from typing import Tuple, List

from parameterized import parameterized

from pdfconduit import Info, Upscale
from pdfconduit.utils.driver import Driver
from tests import *


def scaling_params() -> List[Tuple[str, Driver, float]]:
    return [
        ("{}_{}x".format(driver.name, str(round(scale * 100))), driver, scale)
        for driver in Driver
        for scale in [.5, 1.5, 2.0, 3.0]
    ]


class TestUpscale(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdf_path = pdf_path
        cls.temp = TemporaryDirectory()

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    @parameterized.expand(scaling_params)
    def test_scale(self, name: str, driver: Driver, scale: float):
        scaled = (
            Upscale(
                pdf_path,
                scale=scale,
                suffix=name,
                tempdir=self.temp.name,
            )
            .use(driver)
            .upscale()
        )

        self.assertPdfExists(scaled)
        self.assertPdfScaled(scale, scaled)

    def assertPdfScaled(self, scale, scaled):
        self.assertEqual(
            Info(scaled).size, tuple([i * scale for i in Info(pdf_path).size])
        )
        self.assertEqual(Info(scaled).pages, Info(pdf_path).pages)

    def assertPdfExists(self, scaled):
        self.assertTrue(os.path.isfile(scaled))


if __name__ == "__main__":
    unittest.main()
