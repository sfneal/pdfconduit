from typing import List

from parameterized import parameterized

from tests import PdfconduitTestCase


def slice_params() -> List[str]:
    return [
        "1to1",
        "4to7",
        "2to6",
        "1to8",
        "4to9",
    ]


def slice_name_func(testcase_func, param_num, param):
    return "{}.{}".format(
        testcase_func.__name__,
        param.args[0],
    )


class TestSlice(PdfconduitTestCase):
    @parameterized.expand(slice_params, name_func=slice_name_func)
    def test_slice(self, slice_range: str):
        fp, lp = tuple(slice_range.split("to"))
        fp = int(fp)
        lp = int(lp)

        self.conduit.set_output_suffix("sliced_{}".format(slice_range)).slice(
            fp, lp
        ).write()

        self.assertPdfExists(self.conduit.output)
        self.assertCorrectPagesSliced(fp, lp, self.conduit)
