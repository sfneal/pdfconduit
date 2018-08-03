# importing required modules
from pdfwatermarker.thirdparty.PyPDF2 import PdfFileMerger
import os


def merge(pdfs, output_name, output_dir=None):
    """Merge list of PDF files to a single PDF file."""
    # Create PDF file merger object
    pdf_merger = PdfFileMerger()

    # Appending pdfs one by one
    for pdf in pdfs:
        pdf_merger.append(pdf)

    directory = output_dir if output_dir else os.path.dirname(pdfs[0])
    output = os.path.join(directory, output_name.strip('.pdf') + '.pdf')
    # writing combined pdf to output pdf file
    with open(output, 'wb') as f:
        pdf_merger.write(f)
    return output
