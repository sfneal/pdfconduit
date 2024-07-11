# Write two (2) PDFs to a destination file
from pathlib import Path
from typing import Union

from pypdf import PdfReader as PypdfReader, PdfWriter as PypdfWriter
from pypdf._utils import StrByteType


def write_pdf(pdf_obj: Union[StrByteType, Path], destination: str):
    """
    Write PDF object to file
    :param pdf_obj: PDF object to be written to file
    :param destination: Destination path
    """
    reader = PypdfReader(pdf_obj)  # Create new PDF object
    writer = PypdfWriter()

    page_count = reader.get_num_pages()

    # add the "watermark" (which is the new pdf) on the existing page
    for page_number in range(page_count):
        page = reader.get_page(page_number)
        writer.add_page(page)

    # finally, write "output" to a real file
    with open(destination, "wb") as outputStream:
        writer.write(outputStream)
