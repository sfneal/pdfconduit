# Slice PDF to remove unwanted pages
import os
from tempfile import NamedTemporaryFile

from PyPDF3 import (
    PdfFileReader as Pypdf3FileReader,
    PdfFileWriter as Pypdf3FileWriter,
)
from pypdf import (
    PdfReader as pypdfReader,
    PdfWriter as pypdfWriter,
)

from pdfconduit.utils.info import Info
from pdfconduit.utils.path import add_suffix


def slicer_pypdf3(document, first_page=None, last_page=None, suffix="sliced", tempdir=None):
    """Slice a PDF document to remove pages."""
    # Set output file name
    if tempdir:
        with NamedTemporaryFile(suffix=".pdf", dir=tempdir, delete=False) as temp:
            output = temp.name
    elif suffix:
        output = os.path.join(os.path.dirname(document), add_suffix(document, suffix))
    else:
        with NamedTemporaryFile(suffix=".pdf") as temp:
            output = temp.name

    # Reindex page selections for simple user input
    first_page = first_page - 1 if not None else None

    # Validate page range by comparing selection to number of pages in PDF document
    pages = Info(document).pages
    invalid = (
        "Number of pages: "
        + str(pages)
        + " ----> Page Range Input: "
        + str(first_page)
        + "-"
        + str(last_page)
    )
    assert first_page <= last_page <= pages, invalid

    pdf = Pypdf3FileReader(document)
    writer = Pypdf3FileWriter()

    pages = list(range(pdf.getNumPages()))[first_page:last_page]
    for page in pages:
        writer.addPage(pdf.getPage(page))

    with open(output, "wb") as out:
        writer.write(out)
    return output


def slicer_pypdf(document, first_page=None, last_page=None, suffix="sliced", tempdir=None):
    # Set output file name
    if tempdir:
        with NamedTemporaryFile(suffix=".pdf", dir=tempdir, delete=False) as temp:
            output = temp.name
    elif suffix:
        output = os.path.join(os.path.dirname(document), add_suffix(document, suffix))
    else:
        with NamedTemporaryFile(suffix=".pdf") as temp:
            output = temp.name

    # Reindex page selections for simple user input
    first_page = first_page - 1 if not None else None

    # Validate page range by comparing selection to number of pages in PDF document
    pages = Info(document).pages
    invalid = (
            "Number of pages: "
            + str(pages)
            + " ----> Page Range Input: "
            + str(first_page)
            + "-"
            + str(last_page)
    )
    assert first_page <= last_page <= pages, invalid

    reader = pypdfReader(document)
    writer = pypdfWriter()

    for page_num in list(range(reader.get_num_pages()))[first_page:last_page]:
        writer.add_page(reader.pages[page_num])

    with open(output, "wb") as fp:
        writer.write(fp)

    return output


def slicer(document, first_page=None, last_page=None, suffix="sliced", tempdir=None, method="pypdf3"):
    if method == 'pypdf3':
        return slicer_pypdf3(document, first_page, last_page, suffix, tempdir)
    return slicer_pypdf(document, first_page, last_page, suffix, tempdir)
