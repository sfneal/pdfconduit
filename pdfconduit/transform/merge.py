# Merge PDF documents
import os
from typing import Union, Optional, List

from pdfrw import (
    PdfReader as PdfrwReader,
    PdfWriter as PdfrwWriter,
    IndirectPdfDict as PdfrwIndirectPdfDict,
)
from pypdf import PdfWriter as PyPdfWriter


INPUT_PDFS_TYPE = Union[list, str]


class Merge:
    file: str = None

    def __init__(
        self,
        input_pdfs: INPUT_PDFS_TYPE,
        output_name: str = "merged",
        output_dir: Optional[str] = None,
        method: str = "pdfrw",
    ):
        self.pdfs = self._get_pdf_list(input_pdfs)
        self.directory = output_dir if output_dir else os.path.dirname(self.pdfs[0])
        self.output = os.path.join(
            self.directory, output_name.replace(".pdf", "") + ".pdf"
        )
        self.method = method

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
        if self.method.startswith("pypdf"):
            self.file = self.pypdf(self.pdfs, self.output)
        else:
            self.file = self.pdfrw(self.pdfs, self.output)

        return self.file

    @staticmethod
    def pdfrw(pdf_files: INPUT_PDFS_TYPE, output: str):
        writer = PdfrwWriter()
        for inpfn in pdf_files:
            writer.addpages(PdfrwReader(inpfn).pages)

        writer.trailer.Info = PdfrwIndirectPdfDict(
            Author="Stephen Neal",
            Creator="pdfconduit",
            Producer="pdfconduit",
        )
        writer.write(output)
        return output

    @staticmethod
    def pypdf(pdf_files: INPUT_PDFS_TYPE, output: str):
        merger = PyPdfWriter()

        for pdf in pdf_files:
            merger.append(pdf)

        merger.write(output)
        merger.close()

        return output
