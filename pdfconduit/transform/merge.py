# Merge PDF documents
import os

from pdfrw import (
    PdfReader as PdfrwReader,
    PdfWriter as PdfrwWriter,
    IndirectPdfDict as PdfrwIndirectPdfDict,
)
from pypdf import PdfWriter as PyPdfWriter


class Merge:
    def __init__(
        self, input_pdfs, output_name="merged", output_dir=None, method="pdfrw"
    ):
        self.pdfs = self._get_pdf_list(input_pdfs)
        self.directory = output_dir if output_dir else os.path.dirname(self.pdfs[0])
        self.output = os.path.join(
            self.directory, output_name.replace(".pdf", "") + ".pdf"
        )
        self.method = method
        self.file = self.merge(self.pdfs, self.output)

    def __str__(self):
        return str(self.file)

    @staticmethod
    def validate(pdf):
        if not pdf.startswith(".") and pdf.endswith(".pdf"):
            return True

    def _get_pdf_list(self, input_pdfs):
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

    def merge(self, pdf_files, output):
        """Merge list of PDF files to a single PDF file."""
        if self.method.startswith('pypdf'):
            return self.pypdf(pdf_files, output)
        else:
            return self.pdfrw(pdf_files, output)

    @staticmethod
    def pdfrw(pdf_files, output):
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
    def pypdf(pdf_files, output):
        merger = PyPdfWriter()

        for pdf in pdf_files:
            merger.append(pdf)

        merger.write(output)
        merger.close()

        return output
