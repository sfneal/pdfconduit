from typing import List

from parameterized import parameterized

from pdfconduit import Info
from tests import PdfconduitTestCase


def slice_params() -> List[str]:
    return [
        "1to1",
        "4to7",
        "2to6",
        "1to8",
        "4to9",
    ]



class TestSlice(PdfconduitTestCase):
    @parameterized.expand(slice_params)
    def test_slice(self, slice_range: str):
        fp, lp = tuple(slice_range.split("to"))
        fp = int(fp)
        lp = int(lp)

        self.conduit.set_output_suffix("sliced_{}".format(slice_range)).slice(fp, lp).write()

        self.assertPdfExists(self.conduit.output)
        self.assertCorrectPagesSliced(fp, lp, self.conduit.output)

    def assertCorrectPagesSliced(self, fp, lp, sliced):
        self.assertEqual(Info(sliced).pages, len(range(fp, lp + 1)))