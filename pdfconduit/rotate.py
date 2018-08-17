# Rotate a pdf file
import os
from tempfile import NamedTemporaryFile
from PyPDF3 import PdfFileReader, PdfFileWriter
from pdfconduit.utils import add_suffix


def rotate(file_name, rotate, suffix='rotated', tempdir=None):
    """Rotate PDF by increments of 90 degrees."""
    # Set output file name
    if tempdir:
        outfn = NamedTemporaryFile(suffix='.pdf', dir=tempdir, delete=False).name
    elif suffix:
        outfn = os.path.join(os.path.dirname(file_name), add_suffix(file_name, suffix))
    else:
        outfn = NamedTemporaryFile(suffix='.pdf').name

    with open(file_name, 'rb') as pdf_in:
        pdf_writer = PdfFileWriter()
        pdf_reader = PdfFileReader(pdf_in)
        for pagenum in range(pdf_reader.numPages):
            page = pdf_reader.getPage(pagenum)
            page.rotateClockwise(rotate)
            pdf_writer.addPage(page)

        with open(outfn, 'wb') as pdf_out:
            pdf_writer.write(pdf_out)
    return outfn