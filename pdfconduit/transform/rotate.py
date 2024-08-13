# Rotate a pdf file
import os
from tempfile import NamedTemporaryFile
from pdfconduit.utils.typing import Optional

from pdfrw import (
    PdfReader as PdfrwReader,
    PdfWriter as PdfrwWriter,
)
from pypdf import PdfReader as PypdfReader, PdfWriter as PypdfWriter

from pdfconduit.utils.driver import PdfDriver
from pdfconduit.utils.path import add_suffix


class Rotate(PdfDriver):

    def __init__(
        self,
        file_name: str,
        rotation: int,
        suffix: str = "rotated",
        tempdir: Optional[str] = None,
    ):
        self.file_name = file_name
        self.rotation = rotation
        self.suffix = suffix
        self.tempdir = tempdir

        if tempdir:
            with NamedTemporaryFile(suffix=".pdf", dir=tempdir, delete=False) as temp:
                self.outfn = temp.name
        elif suffix:
            self.outfn = os.path.join(
                os.path.dirname(file_name), add_suffix(file_name, suffix)
            )
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
        trailer = PdfrwReader(self.file_name)
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
        reader = PypdfReader(self.file_name)
        writer = PypdfWriter()

        for page_num in range(1, reader.get_num_pages()):
            writer.add_page(reader.pages[page_num]).rotate(self.rotation)

        with open(self.outfn, "wb") as fp:
            writer.write(fp)

        return self.outfn


def rotate(
    file_name: str,
    rotation: int,
    suffix: str = "rotated",
    tempdir: Optional[str] = None,
    method: str = "pdfrw",
):
    """Rotate PDF by increments of 90 degrees."""
    # todo: remove use of function or clean this up
    rotater = Rotate(file_name, rotation, suffix, tempdir)
    if method == "pdfrw":
        rotater.use_pdfrw()
    else:
        rotater.use_pypdf()
    return rotater.rotate()
