from typing import Tuple, List

from parameterized import parameterized

from pdfconduit import Info
from tests import PdfconduitTestCase


def scale_params() -> List[Tuple[float, bool]]:
    return [(scale, accel) for scale in [0.5, 1.5, 2.0, 3.0] for accel in [True, False]]


def scale_name_func(testcase_func, param_num, param):
    name = "{}_{}x".format(testcase_func.__name__, str(param.args[0]))
    return name + "_accelerate" if param.args[1] else name


class TestScale(PdfconduitTestCase):
    @parameterized.expand(scale_params, name_func=scale_name_func)
    def test_scale(self, scale: float, accelerate: bool):
        suffix = "scaled_{}x".format(scale)
        if accelerate:
            suffix += "_accelerated"

        self.conduit.scale(scale, accelerate=accelerate).set_output_suffix(
            suffix
        ).write()

        self.assertPdfExists(self.conduit.output)
        self.assertPdfScaled(scale, self.conduit.output)

    def assertPdfScaled(self, scale, scaled):
        self.assertEqual(
            Info(scaled).size, tuple([i * scale for i in Info(self.pdf_path).size])
        )
        self.assertEqual(Info(scaled).pages, Info(self.pdf_path).pages)