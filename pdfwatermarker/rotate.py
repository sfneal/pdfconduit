# Rotate a pdf file
from pdfrw import PdfReader, PdfWriter
from pdfwatermarker import set_destination


def rotate(file_name, rotate):
    """Rotate PDF by increments of 90 degrees."""
    outfn = set_destination(file_name, 'rotate')
    trailer = PdfReader(file_name)
    pages = trailer.pages

    ranges = [[1, len(pages)]]

    for onerange in ranges:
        onerange = (onerange + onerange[-1:])[:2]
        for pagenum in range(onerange[0] - 1, onerange[1]):
            pages[pagenum].Rotate = (int(pages[pagenum].inheritable.Rotate or
                                         0) + rotate) % 360

    outdata = PdfWriter(outfn)
    outdata.trailer = trailer
    outdata.write()
    return outfn
