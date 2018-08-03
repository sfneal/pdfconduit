# Slice PDF to remove unwanted pages
import os
from tempfile import NamedTemporaryFile
from pdfwatermarker.thirdparty.PyPDF2 import PdfFileReader, PdfFileWriter


def slicer(document, first_page=None, last_page=None, tempdir=None):
    """Slice a PDF document to remove pages."""
    # Reindex page selections for simple user input
    first_page = first_page - 1 if not None else None
    output = NamedTemporaryFile(suffix='.pdf', dir=tempdir, delete=False)

    pdf = PdfFileReader(document)
    writer = PdfFileWriter()

    pages = list(range(pdf.getNumPages()))[first_page:last_page]
    print(pages)
    for page in pages:
        writer.addPage(pdf.getPage(page))

    with open(output.name, 'wb') as out:
        writer.write(out)
    return output.name
