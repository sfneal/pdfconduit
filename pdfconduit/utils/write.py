# Write two (2) PDFs to a destination file
from PyPDF3 import (
    PdfFileReader as Pypdf3Reader,
    PdfFileWriter as Pypdf3Writer,
)
from pypdf import PdfReader as PypdfReader, PdfWriter as PypdfWriter


def overlay_pdfs(top_pdf, bottom_pdf, destination, use_pypdf=False):
    # todo: possibly remove?
    """
    Overlay PDF objects to files
    :param top_pdf: PDF object to be placed on top
    :param bottom_pdf: PDF file to be placed underneath
    :param destination: Desintation path
    :param use_pypdf:
    """
    if use_pypdf:
        drawing = PypdfReader(top_pdf)  # Create new PDF object
        template = PypdfReader(bottom_pdf)  # read your existing PDF

        # add the "watermark" (which is the new pdf) on the existing page
        page = template.get_page(0)
        page.merge_page(drawing.get_page(0))
        output = PypdfWriter()  # Create new PDF file
        output.add_page(page)

        # finally, write "output" to a real file
        with open(destination, "wb") as outputStream:
            output.write(outputStream)
    else:
        drawing = Pypdf3Reader(top_pdf)  # Create new PDF object
        template = Pypdf3Reader(bottom_pdf)  # read your existing PDF

        # add the "watermark" (which is the new pdf) on the existing page
        page = template.getPage(0)
        page.mergePage(drawing.getPage(0))
        output = Pypdf3Writer()  # Create new PDF file
        output.addPage(page)

        # finally, write "output" to a real file
        with open(destination, "wb") as outputStream:
            output.write(outputStream)


def write_pdf(pdf_obj, destination, use_pypdf=False):
    """
    Write PDF object to file
    :param pdf_obj: PDF object to be written to file
    :param destination: Destination path
    :param use_pypdf:
    """
    if use_pypdf:
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
    else:
        reader = Pypdf3Reader(pdf_obj)  # Create new PDF object
        writer = Pypdf3Writer()

        page_count = reader.getNumPages()

        # add the "watermark" (which is the new pdf) on the existing page
        for page_number in range(page_count):
            page = reader.getPage(page_number)
            writer.addPage(page)

        # finally, write "output" to a real file
        with open(destination, "wb") as outputStream:
            writer.write(outputStream)
