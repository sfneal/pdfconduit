# Retrieve information about a PDF document
from pdfwatermarker.thirdparty.PyPDF2 import PdfFileReader


def number_of_pages(path):
    """Retrieve PDF number of pages"""
    return PdfFileReader(path).getNumPages()


def metadata(path):
    """Retrieve PDF metadata"""
    return PdfFileReader(path).getDocumentInfo()


def resources(path):
    """Retrieve contents of each page of PDF"""
    pdf = PdfFileReader(path)
    return [pdf.getPage(i) for i in range(pdf.getNumPages)]


def text_extractor(path):
    """Extract text from a PDF file"""
    pdf = PdfFileReader(path)
    return [pdf.getPage(i).extractText() for i in range(PdfFileReader(path).getNumPages)]


def security_objects(path, password='baz'):
    """Print security object information for a pdf document"""
    pdf = PdfFileReader(path)
    pdf.decrypt(password)
    for k in pdf.resolvedObjects.items():
        print(k[0])
        for i, v in k[1].items():
            print(i, '-->', v)


def get_pdf_size(file_name):
    """Get width and height of a PDF"""
    try:
        size = PdfFileReader(file_name).getPage(0).mediaBox
    except AttributeError:
        size = file_name.getPage(0).mediaBox
    return {'w': float(size[2]), 'h': float(size[3])}
