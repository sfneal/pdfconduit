# Retrieve information about a PDF document
from PyPDF3 import PdfFileReader
from pdfconduit.utils.read import pypdf_reader
from pdfconduit.utils._permissions import Permissions


class Info:
    def __init__(self, path, password=None, use_pypdf=False):
        self.use_pypdf = use_pypdf
        if use_pypdf:
            self.pdf = pypdf_reader(path, password)
        else:
            self.pdf = self._pypdf3_reader(path, password)

    @staticmethod
    def _pypdf3_reader(path, password):
        """Read PDF and decrypt if encrypted."""
        pdf = PdfFileReader(path) if not isinstance(path, PdfFileReader) else path
        if password:
            pdf.decrypt(password)
        return pdf

    @staticmethod
    def _resolved_objects(pdf, xobject):
        """Retrieve rotatation info."""
        return [pdf.getPage(i).get(xobject) for i in range(pdf.getNumPages())][0]

    @property
    def encrypted(self):
        """Check weather a PDF is encrypted"""
        if self.use_pypdf:
            return self.pdf.is_encrypted
        return self.pdf.isEncrypted

    @property
    def decrypted(self):
        """Check weather a PDF is encrypted"""
        return not self.encrypted

    @property
    def pages(self):
        """Retrieve PDF number of pages"""
        return self.pdf.getNumPages()

    @property
    def metadata(self):
        """Retrieve PDF metadata"""
        if self.use_pypdf:
            return self.pdf.metadata
        return self.pdf.getDocumentInfo()

    def resources(self):
        """Retrieve contents of each page of PDF"""
        # todo: refactor to generator?
        return [self.pdf.getPage(i) for i in range(self.pdf.getNumPages())]

    @property
    def security(self):
        """Print security object information for a pdf document"""
        if self.use_pypdf:
            return {
                k: v for i in self.pdf.resolved_objects.items() for k, v in i[1].items()
            }
        return {k: v for i in self.pdf.resolvedObjects.items() for k, v in i[1].items()}

    @property
    def dimensions(self):
        """Get width and height of a PDF"""
        # todo: add page parameter?
        # todo: add height & width methods?
        size = self.pdf.getPage(0).mediaBox
        return {"w": float(size[2]), "h": float(size[3])}

    @property
    def size(self):
        """Get width and height of a PDF"""
        size = self.pdf.getPage(0).mediaBox
        return float(size[2]), float(size[3])

    @property
    def rotate(self):
        """Retrieve rotation info."""
        # todo: add page param
        # todo: refactor to `rotation()`
        # todo: add is_rotated
        return self._resolved_objects(self.pdf, "/Rotate")

    @property
    def permissions(self):
        """Retrieve user access permissions."""
        return Permissions(self.pdf)
