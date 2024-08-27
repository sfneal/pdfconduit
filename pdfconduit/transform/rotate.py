# Rotate a pdf file
import os
from io import BytesIO
from tempfile import NamedTemporaryFile
from typing import Optional

from pdfrw import (
    PdfReader as PdfrwReader,
    PdfWriter as PdfrwWriter,
)
from pypdf import PdfReader as PypdfReader, PdfWriter as PypdfWriter

from pdfconduit.utils.driver import PdfDriver
from pdfconduit.utils.path import add_suffix
from pdfconduit.utils.typing import PdfObject


class Rotate(PdfDriver):

    def __init__(
        self,
        pdf: PdfObject,
        rotation: int,
        suffix: str = "rotated",
        tempdir: Optional[str] = None,
        output: Optional[str] = None,
    ):
        self.pdf_object = pdf
        self.rotation = rotation
        self.suffix = suffix

        if output:
            self.outfn = output
        else:
            self.tempdir = tempdir

            if tempdir:
                with NamedTemporaryFile(
                    suffix=".pdf", dir=tempdir, delete=False
                ) as temp:
                    self.outfn = temp.name
            elif suffix:
                self.outfn = os.path.join(os.path.dirname(pdf), add_suffix(pdf, suffix))
            else:
                self.outfn = NamedTemporaryFile(suffix=".pdf").name

    def __str__(self) -> str:
        return self.file

    def rotate(self) -> str:
        return self.execute()

    @property
    def file(self) -> str:
        return str(self.outfn)

    def pdfrw(self) -> str:
        if isinstance(self.pdf_object, BytesIO):
            trailer = PdfrwReader(fdata=self.pdf_object.getvalue())
        else:
            trailer = PdfrwReader(fname=self.pdf_object)

        pages = trailer.pages

        ranges = [[1, len(pages)]]

        for onerange in ranges:
            onerange = (onerange + onerange[-1:])[:2]
            for pagenum in range(onerange[0] - 1, onerange[1]):
                pages[pagenum].Rotate = (
                    int(pages[pagenum].inheritable.Rotate or 0) + self.rotation
                ) % 360

        outdata = PdfrwWriter(self.outfn)
        outdata.trailer = trailer
        outdata.write()
        return self.outfn

    def pypdf(self) -> str:
        reader = PypdfReader(self.pdf_object)
        writer = PypdfWriter()

        for page_num in range(1, reader.get_num_pages()):
            writer.add_page(reader.pages[page_num]).rotate(self.rotation)

        with open(self.outfn, "wb") as fp:
            writer.write(fp)

        return self.outfn
