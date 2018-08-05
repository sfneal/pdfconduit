# Merge PDF documents
import os
from pdfwatermarker.thirdparty.PyPDF2 import PdfFileMerger


class Merge:
    def __init__(self, input_pdfs, output_name='merged', output_dir=None):
        self.pdfs = self._get_pdf_list(input_pdfs)
        self.directory = output_dir if output_dir else os.path.dirname(self.pdfs[0])
        self.output = os.path.join(self.directory, output_name.strip('.pdf') + '.pdf')
        self.merge(self.pdfs, self.output)

    @staticmethod
    def validate(pdf):
        if not pdf.startswith('.') and pdf.endswith('.pdf'):
            return True

    def _get_pdf_list(self, input_pdfs):
        """
        Generate list of PDF documents.

        :param input_pdfs: List of PDFs or a directory path
             Directory - Scans directory contents
             List - Filters list to assert all list items are paths to PDF documents
        :return: List of PDF paths
        """
        if os.path.isdir(input_pdfs):
            return [os.path.join(input_pdfs, pdf) for pdf in os.listdir(input_pdfs) if self.validate(pdf)]
        else:
            return [pdf for pdf in input_pdfs if self.validate(pdf)]

    @staticmethod
    def merge(pdf_files, output):
        """Merge list of PDF files to a single PDF file."""
        # Create PDF file merger object
        pdf_merger = PdfFileMerger()

        # Appending pdfs one by one
        for pdf in pdf_files:
            pdf_merger.append(pdf)

        # writing combined pdf to output pdf file
        with open(output, 'wb') as f:
            pdf_merger.write(f)
        return output


def main():
    from pdfwatermarker.utils.gui import get_directory
    d = get_directory()
    m = Merge(d)
    print(m.output)


if __name__ == '__main__':
    main()
