# Retrieve information about a PDF document
from PyPDF3 import PdfFileReader


def _reader(path, password=None, prompt=True):
    """Read PDF and decrypt if encrypted."""
    pdf = PdfFileReader(path)
    # Check that PDF is encrypted
    if pdf.isEncrypted:
        # Check that password is none
        if not password:
            pdf.decrypt('')
            # Try and decrypt PDF using no password, prompt for password
            if pdf.isEncrypted and prompt:
                print('No password has been given for encrypted PDF ', path)
                password = input('Enter Password: ')
            else:
                return False
        pdf.decrypt(password)
    return pdf


def _resolved_objects(pdf, object):
    """Retrieve rotatation info."""
    return [pdf.getPage(i).get(object) for i in range(pdf.getNumPages())][0]


def encrypted(path):
    """Check weather a PDF is encrypted"""
    return True if not _reader(path, prompt=False) else False


def pages(path, password=None):
    """Retrieve PDF number of pages"""
    return _reader(path, password).getNumPages()


def metadata(path, password=None):
    """Retrieve PDF metadata"""
    return _reader(path, password).getDocumentInfo()


def resources(path, password=None):
    """Retrieve contents of each page of PDF"""
    pdf = _reader(path, password)
    return [pdf.getPage(i) for i in range(pages(path, password))]


def security(path, password=None):
    """Print security object information for a pdf document"""
    pdf = _reader(path, password)
    return {k: v for i in pdf.resolvedObjects.items() for k, v in i[1].items()}


def dimensions(path, password=None):
    """Get width and height of a PDF"""
    try:
        size = _reader(path, password).getPage(0).mediaBox
    except AttributeError:
        size = path.getPage(0).mediaBox
    return {'w': float(size[2]), 'h': float(size[3])}


def rotate(path, password=None):
    """Retrieve rotation info."""
    return _resolved_objects(_reader(path, password), '/Rotate')
