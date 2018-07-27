# Write two (2) PDFs to a destination file
from pdfwatermarker.thirdparty.PyPDF2 import PdfFileWriter, PdfFileReader


def write_pdf(top_pdf, bottom_pdf, destination):
    """
    Write PDF objects to files
    :param top_pdf: PDF object to be placed on top
    :param bottom_pdf: PDF file to be placed underneath
    :param destination: Desintation path
    """
    drawing = PdfFileReader(top_pdf)  # Create new PDF object
    template = PdfFileReader(open(bottom_pdf, "rb"))  # read your existing PDF

    # add the "watermark" (which is the new pdf) on the existing page
    page = template.getPage(0)
    page.mergePage(drawing.getPage(0))
    output = PdfFileWriter()  # Create new PDF file
    output.addPage(page)

    # finally, write "output" to a real file
    with open(destination, "wb") as outputStream:
        output.write(outputStream)
    outputStream.close()
