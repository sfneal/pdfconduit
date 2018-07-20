# Upscale a PDF file
from pdfrw import PdfReader, PdfWriter, PageMerge, IndirectPdfDict
from pdfwatermarker import set_destination


def upscale(file_name, margin=0, scale=1.5):
    """Upscale a PDF to a large size."""
    def adjust(page):
        info = PageMerge().add(page)
        x1, y1, x2, y2 = info.xobj_box
        viewrect = (margin, margin, x2 - x1 - 2 * margin, y2 - y1 - 2 * margin)
        page = PageMerge().add(page, viewrect=viewrect)
        page[0].scale(scale)
        return page.render()

    output = set_destination(file_name, 'upscaled')
    reader = PdfReader(file_name)
    writer = PdfWriter(output)
    for i in list(range(0, len(reader.pages))):
        writer.addpage(adjust(reader.pages[i]))
    writer.trailer.Info = IndirectPdfDict(reader.Info or {})
    writer.write()
    return output
