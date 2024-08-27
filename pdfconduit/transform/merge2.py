# Merge PDF documents
from io import BytesIO

from pdfrw import (
    PdfReader as PdfrwReader,
    PdfWriter as PdfrwWriter,
    IndirectPdfDict as PdfrwIndirectPdfDict,
)
from pypdf import PdfWriter as PyPdfWriter

from pdfconduit.utils.driver import PdfDriver
from pdfconduit.utils.typing import PdfObjects


class Merge2(PdfDriver):
    def __init__(self, pdfs: PdfObjects, output: str):
        self._pdfs = pdfs
        self._output = output

    def merge(self) -> str:
        """Merge list of PDF files to a single PDF file."""
        return self.execute()

    def pdfrw(self):
        writer = PdfrwWriter()

        for pdf_object in self._pdfs:
            if isinstance(pdf_object, BytesIO):
                reader = PdfrwReader(fdata=pdf_object.getvalue())
            else:
                reader = PdfrwReader(fname=pdf_object)
            writer.addpages(reader.pages)

        writer.trailer.Info = PdfrwIndirectPdfDict(
            Author="Stephen Neal",
            Creator="pdfconduit",
            Producer="pdfconduit",
        )
        writer.write(self._output)
        return self._output

    def pypdf(self):
        merger = PyPdfWriter()

        for pdf in self._pdfs:
            merger.append(pdf)

        merger.write(self._output)
        merger.close()

        return self._output
