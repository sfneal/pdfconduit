# Retrieve information about a PDF document
from typing import Optional, List, Dict, Tuple, Union

from pypdf import PdfReader, DocumentInformation, PageObject, PdfWriter

from pdfconduit.utils._permissions import Permissions
from pdfconduit.utils.read import pypdf_reader


class Info:
    def __init__(
        self, pdf: Union[str, PdfReader, PdfWriter], password: Optional[str] = None
    ):
        self.pdf = (
            pdf
            if isinstance(pdf, (PdfReader, PdfWriter))
            else pypdf_reader(pdf, password)
        )

    @staticmethod
    def _resolved_objects(pdf: PdfReader, xobject: str) -> int:
        """Retrieve rotation info."""
        return [pdf.get_page(i).get(xobject) for i in range(pdf.get_num_pages())][0]

    @property
    def encrypted(self) -> bool:
        """Check weather a PDF is encrypted"""
        return self.pdf.is_encrypted

    @property
    def decrypted(self) -> bool:
        """Check weather a PDF is encrypted"""
        return not self.encrypted

    @property
    def pages(self) -> int:
        """Retrieve PDF number of pages"""
        return self.pdf.get_num_pages()

    @property
    def metadata(self) -> Optional[DocumentInformation]:
        """Retrieve PDF metadata"""
        return self.pdf.metadata

    def resources(self) -> List[PageObject]:
        """Retrieve contents of each page of PDF"""
        # todo: refactor to generator?
        return [self.pdf.get_page(i) for i in range(self.pdf.get_num_pages())]

    @property
    def security(self) -> Dict[str, int]:
        """Print security object information for a pdf document"""
        return {
            k: v for i in self.pdf.resolved_objects.items() for k, v in i[1].items()
        }

    @property
    def dimensions(self) -> Dict[str, float]:
        """Get width and height of a PDF"""
        # todo: add page parameter?
        # todo: add height & width methods?
        # todo: add typed dict
        size = self.pdf.get_page(0).mediabox
        return {"w": float(size[2]), "h": float(size[3])}

    @property
    def size(self) -> Tuple[float, float]:
        """Get width and height of a PDF"""
        size = self.pdf.get_page(0).mediabox

        return float(size[2]), float(size[3])

    @property
    def rotate(self) -> int:
        """Retrieve rotation info."""
        # todo: add page param
        # todo: refactor to `rotation()`
        # todo: add is_rotated
        return self._resolved_objects(self.pdf, "/Rotate")

    @property
    def permissions(self) -> Permissions:
        """Retrieve user access permissions."""
        return Permissions(self.pdf)

    @property
    def images_count(self) -> int:
        return sum([len(page.images) for page in self.pdf.pages])
