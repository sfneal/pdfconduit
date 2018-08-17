# Upscale a PDF file
from tempfile import NamedTemporaryFile
from pdfrw import PdfReader, PdfWriter, PageMerge, IndirectPdfDict
from PyPDF3 import PdfFileReader, PdfFileWriter
from PyPDF3.pdf import PageObject
from pdfconduit.utils import Info


def upscale(file_name, margin=0, margin_x=0, margin_y=0, scale=1.5, method='pypdf3', tempdir=None):
    """Upscale a PDF to a large size."""
    # Output file name
    output = NamedTemporaryFile(suffix='.pdf', dir=tempdir, delete=False)

    def pdfrw():
        def adjust(page):
            info = PageMerge().add(page)
            x1, y1, x2, y2 = info.xobj_box
            viewrect = (margin, margin, x2 - x1 - 2 * margin, y2 - y1 - 2 * margin)
            page = PageMerge().add(page, viewrect=viewrect)
            page[0].scale(scale)
            return page.render()

        reader = PdfReader(file_name)
        writer = PdfWriter(output)
        for i in list(range(0, len(reader.pages))):
            writer.addpage(adjust(reader.pages[i]))
        writer.trailer.Info = IndirectPdfDict(reader.Info or {})
        writer.write()

    def pypdf3():
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

        with open(output.name, "wb") as outputStream:
            writer.write(outputStream)

    if method is 'pypdf3':
        pypdf3()
    else:
        pdfrw()
    return output.name
