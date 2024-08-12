import os.path
import random
from typing import Iterable, List

from parameterized import parameterized

from pdfconduit import Conduit, Info
from tests.pdfconduit import PdfconduitTestCase
from .. import test_data_path


def rotate_params() -> List[int]:
    return [
        90,
        180,
        270,
    ]


def rotate_exact_params() -> List[int]:
    return list(
        map(lambda rotation: rotation + random.randrange(10, 80), rotate_params())
    )


def rotate_name_func(testcase_func, param_num, param):
    return "{}_{}".format(
        testcase_func.__name__,
        param_num,
        param.args[0],
    )


class TestRotate(PdfconduitTestCase):
    @parameterized.expand(rotate_params, name_func=rotate_name_func)
    def test_can_rotate(self, rotation: int):
        self.conduit.rotate(rotation).set_output_suffix(
            "rotated_{}".format(rotation)
        ).write()

        self.assertPdfExists(self.conduit.output)
        self.assertPdfRotation(self.conduit.output, rotation)

    @parameterized.expand(rotate_exact_params, name_func=rotate_name_func)
    def test_can_rotate_exact(self, rotation: int):
        self.conduit.rotate_exact(rotation).set_output_suffix(
            "rotated_{}".format(rotation)
        ).write()

        self.assertPdfExists(self.conduit.output)
        self.assertPdfRotation(self.conduit.output, rotation)

    @parameterized.expand(rotate_exact_params, name_func=rotate_name_func)
    def test_cannot_rotate(self, rotation: int):
        with self.assertRaises(ValueError) as context:
            self.conduit.rotate(rotation).write()

        self.assertPdfDoesntExists(self.conduit.output)
        self.assertTrue(
            "Rotation angle must be a multiple of 90" in str(context.exception)
        )

    def assertPdfRotation(self, rotated, rotation):
        self.assertEqual(Info(rotated).rotate, rotation)
