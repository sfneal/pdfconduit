# Upscale a PDF file
import os
from tempfile import NamedTemporaryFile
from PyPDF3 import PdfFileReader, PdfFileWriter
from PyPDF3.pdf import PageObject
from pdfconduit.utils import Info, add_suffix


def upscale(file_name, margin_x=0, margin_y=0, scale=1.5, suffix='scaled', tempdir=None):
    """Upscale a PDF to a large size."""
    # Set output file name
    if tempdir:
        output = NamedTemporaryFile(suffix='.pdf', dir=tempdir, delete=False).name
    elif suffix:
        output = os.path.join(os.path.dirname(file_name), add_suffix(file_name, suffix))
    else:
        output = NamedTemporaryFile(suffix='.pdf').name

    reader = PdfFileReader(file_name)
    writer = PdfFileWriter()
    dims = Info(file_name).dimensions
    target_w = dims['w'] * scale
    target_h = dims['h'] * scale

    # Number of pages in input document
    page_count = reader.getNumPages()

    for page_number in range(page_count):
        wtrmrk = reader.getPage(page_number)

        page = PageObject.createBlankPage(width=target_w, height=target_h)
        page.mergeScaledTranslatedPage(wtrmrk, scale, margin_x, margin_y)
        writer.addPage(page)

    with open(output, "wb") as outputStream:
        writer.write(outputStream)
    return output
