# Upscale a PDF file
import os
from tempfile import NamedTemporaryFile
from typing import Optional

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
from pdfconduit.utils.path import add_suffix


class Upscale(PdfDriver):
    def __init__(
        self,
        file_name: str,
        margin_x: int = 0,
        margin_y: int = 0,
        scale: float = 1.5,
        suffix: str = "scaled",
        tempdir: Optional[str] = None,
    ):
        self.file_name = file_name
        self.margin_x = margin_x
        self.margin_y = margin_y
        self.scale = scale
        self.suffix = suffix

        # Set output file name
        if tempdir:
            with NamedTemporaryFile(
                suffix="_" + suffix + ".pdf", dir=tempdir, delete=False
            ) as temp:
                self.output = temp.name
        elif suffix:
            self.output = os.path.join(
                os.path.dirname(file_name), add_suffix(file_name, suffix)
            )
        else:
            self.output = NamedTemporaryFile(suffix="_" + suffix + ".pdf").name

        # Get target width and height
        dims = Info(self.file_name).dimensions
        self.target_w = dims["w"] * self.scale
        self.target_h = dims["h"] * self.scale

    def __str__(self) -> str:
        return self.file

    def upscale(self) -> str:
        # Execute either pdfrw or PyPDF3 method
        return self.execute()

    @property
    def file(self) -> str:
        return str(self.output)

    def _pdfrw_adjust(self, page: object):
        info = pdfrwPageMerge().add(page)
        x1, y1, x2, y2 = info.xobj_box
        viewrect = (
            self.margin_x,
            self.margin_y,
            x2 - x1 - 2 * self.margin_x,
            y2 - y1 - 2 * self.margin_y,
        )
        page = pdfrwPageMerge().add(page, viewrect=viewrect)
        page[0].scale(self.scale)
        return page.render()

    def pdfrw(self) -> str:
        reader = pdfrwReader(self.file_name)
        writer = pdfrwWriter(self.output)
        for i in list(range(0, len(reader.pages))):
            writer.addpage(self._pdfrw_adjust(reader.pages[i]))
        writer.trailer.Info = pdfrwIndirectPdfDict(reader.Info or {})
        writer.write()

        return self.output

    def pypdf(self) -> str:
        reader = pypdfReader(self.file_name)
        writer = pypdfWriter()

        for page_num in range(0, reader.get_num_pages()):
            page = reader.pages[page_num]

            page.scale_to(width=self.target_w, height=self.target_h)

            writer.add_page(page)

        with open(self.output, "wb") as fp:
            writer.write(fp)

        return self.output
