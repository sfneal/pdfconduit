# Slice PDF to remove unwanted pages
import os
from tempfile import NamedTemporaryFile

from pypdf import (
    PdfReader as pypdfReader,
    PdfWriter as pypdfWriter,
)

from pdfconduit.utils.info import Info
from pdfconduit.utils.path import add_suffix


def slicer(
    document,
    first_page=None,
    last_page=None,
    suffix="sliced",
    tempdir=None,
):
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
