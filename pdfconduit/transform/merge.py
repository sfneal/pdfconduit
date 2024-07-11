# Merge PDF documents
import os
from typing import Union, Optional, List

from pdfrw import (
    PdfReader as PdfrwReader,
    PdfWriter as PdfrwWriter,
    IndirectPdfDict as PdfrwIndirectPdfDict,
)
from pypdf import PdfWriter as PyPdfWriter

from pdfconduit.utils.driver import PdfDriver

INPUT_PDFS_TYPE = Union[list, str]


class Merge(PdfDriver):
    file: str = None

    def __init__(
        self,
        input_pdfs: INPUT_PDFS_TYPE,
        output_name: str = "merged",
        output_dir: Optional[str] = None,
    ):
        self.pdfs = self._get_pdf_list(input_pdfs)
        self.directory = output_dir if output_dir else os.path.dirname(self.pdfs[0])
        self.output = os.path.join(
            self.directory, output_name.replace(".pdf", "") + ".pdf"
        )

    def __str__(self) -> str:
        return str(self.file)

    @staticmethod
    def validate(pdf) -> bool:
        # todo: simplify logic?
        if not pdf.startswith(".") and pdf.endswith(".pdf"):
            return True

    def _get_pdf_list(self, input_pdfs: INPUT_PDFS_TYPE) -> List[str]:
        """
        Generate list of PDF documents.

        :param input_pdfs: List of PDFs or a directory path
             Directory - Scans directory contents
             List - Filters list to assert all list items are paths to PDF documents
        :return: List of PDF paths
        """
        if isinstance(input_pdfs, list):
            return [pdf for pdf in input_pdfs if self.validate(pdf)]
        elif os.path.isdir(input_pdfs):
            return [
                os.path.join(input_pdfs, pdf)
                for pdf in os.listdir(input_pdfs)
                if self.validate(pdf)
            ]
        # todo: raise error if conditions aren't met?

    def merge(self) -> str:
        """Merge list of PDF files to a single PDF file."""
        self.file = self.execute()
        return self.file

    def pdfrw(self):
        writer = PdfrwWriter()
        for inpfn in self.pdfs:
            writer.addpages(PdfrwReader(inpfn).pages)

        writer.trailer.Info = PdfrwIndirectPdfDict(
            Author="Stephen Neal",
            Creator="pdfconduit",
            Producer="pdfconduit",
        )
        writer.write(self.output)
        return self.output

    def pypdf(self):
        merger = PyPdfWriter()

        for pdf in self.pdfs:
            merger.append(pdf)

        merger.write(self.output)
        merger.close()

        return self.output
