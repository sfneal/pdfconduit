# Retrieve information about a PDF document
from pdfconduit.utils._permissions import Permissions
from pdfconduit.utils.read import pypdf_reader


class Info:
    def __init__(self, path, password=None):
        self.pdf = pypdf_reader(path, password)

    @staticmethod
    def _resolved_objects(pdf, xobject):
        """Retrieve rotation info."""
        return [pdf.get_page(i).get(xobject) for i in range(pdf.get_num_pages())][0]

    @property
    def encrypted(self):
        """Check weather a PDF is encrypted"""
        return self.pdf.is_encrypted

    @property
    def decrypted(self):
        """Check weather a PDF is encrypted"""
        return not self.encrypted

    @property
    def pages(self):
        """Retrieve PDF number of pages"""
        return self.pdf.get_num_pages()

    @property
    def metadata(self):
        """Retrieve PDF metadata"""
        return self.pdf.metadata

    def resources(self):
        """Retrieve contents of each page of PDF"""
        # todo: refactor to generator?
        return [self.pdf.get_page(i) for i in range(self.pdf.get_num_pages())]

    @property
    def security(self):
        """Print security object information for a pdf document"""
        return {k: v for i in self.pdf.resolved_objects.items() for k, v in i[1].items()}

    @property
    def dimensions(self):
        """Get width and height of a PDF"""
        # todo: add page parameter?
        # todo: add height & width methods?
        size = self.pdf.get_page(0).mediabox
        return {"w": float(size[2]), "h": float(size[3])}

    @property
    def size(self):
        """Get width and height of a PDF"""
        size = self.pdf.get_page(0).mediabox

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
