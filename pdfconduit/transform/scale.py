# Upscale a PDF file
from io import BytesIO

from pdfrw import (
    PdfReader as pdfrwReader,
    PdfWriter as pdfrwWriter,
    PageMerge as pdfrwPageMerge,
    IndirectPdfDict as pdfrwIndirectPdfDict,
)
from pypdf import (
    PdfReader as pypdfReader,
    PdfWriter as pypdfWriter,
)

from pdfconduit.utils.driver import PdfDriver
from pdfconduit.utils.info import Info
from pdfconduit.utils.typing import PdfObject


class Scale(PdfDriver):
    def __init__(
        self,
        pdf: PdfObject,
        output: str,
        scale: float = 1.5,
        margin_x: int = 0,
        margin_y: int = 0,
    ):
        self._pdf = pdf
        self._output = output
        self._margin_x = margin_x
        self._margin_y = margin_y
        self._scale = scale

    def upscale(self) -> str:
        # Execute either pdfrw or PyPDF3 method
        return self.execute()

    def _pdfrw_adjust(self, page: object):
        info = pdfrwPageMerge().add(page)
        x1, y1, x2, y2 = info.xobj_box
        viewrect = (
            self._margin_x,
            self._margin_y,
            x2 - x1 - 2 * self._margin_x,
            y2 - y1 - 2 * self._margin_y,
        )
        page = pdfrwPageMerge().add(page, viewrect=viewrect)
        page[0].scale(self._scale)
        return page.render()

    def pdfrw(self) -> str:
        if isinstance(self._pdf, BytesIO):
            reader = pdfrwReader(fdata=self._pdf.getvalue())
        else:
            reader = pdfrwReader(fname=self._pdf)

        writer = pdfrwWriter(self._output)

        for i in list(range(0, len(reader.pages))):
            writer.addpage(self._pdfrw_adjust(reader.pages[i]))

        writer.trailer.Info = pdfrwIndirectPdfDict(reader.Info or {})
        writer.write()

        return self._output

    def pypdf(self) -> str:
        reader = pypdfReader(self._pdf)

        # Get target width and height
        dims = Info(reader).dimensions
        target_w = dims["w"] * self._scale
        target_h = dims["h"] * self._scale

        writer = pypdfWriter()

        for page_num in range(0, reader.get_num_pages()):
            page = reader.pages[page_num]
            page.scale_to(width=target_w, height=target_h)
            writer.add_page(page)

        with open(self._output, "wb") as fp:
            writer.write(fp)

        return self._output
