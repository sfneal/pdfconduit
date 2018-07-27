# importing required modules
from pdfwatermarker.thirdparty.PyPDF2 import PdfFileMerger
import os


def merge(pdfs, output_name):
    """Merge list of PDF files to a single PDF file."""
    # Create PDF file merger object
    pdf_merger = PdfFileMerger()

    # Appending pdfs one by one
    for pdf in pdfs:
        pdf_merger.append(pdf)

    output = os.path.join(os.path.dirname(pdfs[0]), output_name.strip('.pdf') + '.pdf')
    # writing combined pdf to output pdf file
    with open(output, 'wb') as f:
        pdf_merger.write(f)
