# Rotate a pdf file
from tempfile import NamedTemporaryFile
from pdfwatermarker.thirdparty.PyPDF2 import PdfFileReader, PdfFileWriter
from pdfrw import PdfReader, PdfWriter


def rotate(file_name, rotate, method='pypdf2', tempdir=None):
    """Rotate PDF by increments of 90 degrees."""
    outfn = NamedTemporaryFile(suffix='.pdf', dir=tempdir)

    def pypdf2():
        pdf_in = open(file_name, 'rb')
        pdf_reader = PdfFileReader(pdf_in)
        pdf_writer = PdfFileWriter()
        for pagenum in range(pdf_reader.numPages):
            page = pdf_reader.getPage(pagenum)
            page.rotateClockwise(rotate)
            pdf_writer.addPage(page)
        pdf_out = open(outfn, 'wb')
        pdf_writer.write(pdf_out)
        pdf_out.close()
        pdf_in.close()
        return outfn

    def pdfrw():
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

    if method is 'pypdf2':
        return pypdf2()
    else:
        return pdfrw()
