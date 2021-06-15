# Write two (2) PDFs to a destination file
from PyPDF3 import PdfFileWriter, PdfFileReader


def overlay_pdfs(top_pdf, bottom_pdf, destination):
    """
    Overlay PDF objects to files
    :param top_pdf: PDF object to be placed on top
    :param bottom_pdf: PDF file to be placed underneath
    :param destination: Desintation path
    """
    drawing = PdfFileReader(top_pdf)  # Create new PDF object
    template = PdfFileReader(bottom_pdf)  # read your existing PDF

    # add the "watermark" (which is the new pdf) on the existing page
    page = template.getPage(0)
    page.mergePage(drawing.getPage(0))
    output = PdfFileWriter()  # Create new PDF file
    output.addPage(page)

    # finally, write "output" to a real file
    with open(destination, "wb") as outputStream:
        output.write(outputStream)


def write_pdf(pdf_obj, destination):
    """
    Write PDF object to file
    :param pdf_obj: PDF object to be written to file
    :param destination: Desintation path
    """
    reader = PdfFileReader(pdf_obj)  # Create new PDF object
    writer = PdfFileWriter()

    page_count = reader.getNumPages()

    # add the "watermark" (which is the new pdf) on the existing page
    for page_number in range(page_count):
        page = reader.getPage(page_number)
        writer.addPage(page)

    # finally, write "output" to a real file
    with open(destination, "wb") as outputStream:
        writer.write(outputStream)
