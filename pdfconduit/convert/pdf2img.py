# Convert each page of PDF to images
import os
from enum import Enum
from io import BytesIO
from tempfile import NamedTemporaryFile
from typing import List, Optional

import fitz
from PIL import Image
from pymupdf import Document as PyMupdfDocument

from pdfconduit.utils.path import add_suffix
from pdfconduit.utils.typing import PdfObject


class ImageExtension(Enum):
    PNG: str = "png"
    JPG: str = "jpg"


class PDF2IMG:
    _filename: str = None
    _tempfile: Optional[NamedTemporaryFile] = None
    _doc: PyMupdfDocument

    def __init__(
        self,
        pdf: PdfObject,
        output: Optional[str] = None,
        ext: ImageExtension = ImageExtension.PNG,
        alpha: bool = False,
    ):
        self._pdf = pdf
        self._directory = output
        self._ext = ext.value
        self._alpha = alpha

        if isinstance(self._pdf, BytesIO):
            self._tempfile = NamedTemporaryFile(
                suffix=self._ext, dir=self._directory, delete=False
            )
            self._filename = self._tempfile.name
            self._directory = os.path.dirname(self._filename)
            self._doc = fitz.open(stream=self._pdf)
        else:
            self._filename = os.path.basename(self._pdf)
            self._directory = os.path.dirname(self._pdf)
            self._doc = fitz.open(filename=self._pdf)

    def convert(self):
        saved = []
        for index, image in enumerate(self._get_pdf_data()):
            output = os.path.join(
                self._directory,
                add_suffix(self._filename, str(index + 1), ext=self._ext),
            )
            with Image.open(BytesIO(image)) as pillow:
                pillow.save(output)
            saved.append(output)
        self._doc.close()
        if self._tempfile:
            self._tempfile.close()
        return saved

    def _get_pdf_data(self) -> List[bytes]:
        return FitzPdfToImage(self._doc, self._alpha).convert()


class FitzPdfToImage:
    def __init__(self, doc: PyMupdfDocument, alpha: bool = False):
        self._doc = doc
        self._dlist_tab = [None] * len(doc)
        self._alpha = alpha

    def convert(self) -> List[bytes]:
        return [self._get_page_data(cur_page) for cur_page in range(len(self._doc))]

    def _get_page_data(self, pno, zoom=0) -> bytes:
        """
        Return a PNG image for a document page number. If zoom is other than 0, one of
        the 4 page quadrants are zoomed-in instead and the corresponding clip returned.
        """
        dlist = self._dlist_tab[pno]  # get display list
        if not dlist:  # create if not yet there
            self._dlist_tab[pno] = self._doc[pno].get_displaylist()
            dlist = self._dlist_tab[pno]
        r = dlist.rect  # page rectangle
        mp = r.tl + (r.br - r.tl) * 0.5  # rect middle point
        mt = r.tl + (r.tr - r.tl) * 0.5  # middle of top edge
        ml = r.tl + (r.bl - r.tl) * 0.5  # middle of left edge
        mr = r.tr + (r.br - r.tr) * 0.5  # middle of right egde
        mb = r.bl + (r.br - r.bl) * 0.5  # middle of bottom edge
        mat = fitz.Matrix(2, 2)  # zoom matrix
        if zoom == 1:  # top-left quadrant
            clip = fitz.Rect(r.tl, mp)
        elif zoom == 4:  # bot-right quadrant
            clip = fitz.Rect(mp, r.br)
        elif zoom == 2:  # top-right
            clip = fitz.Rect(mt, mr)
        elif zoom == 3:  # bot-left
            clip = fitz.Rect(ml, mb)
        if zoom == 0:  # total page
            pix = dlist.get_pixmap(alpha=self._alpha)
        else:
            pix = dlist.get_pixmap(alpha=self._alpha, matrix=mat, clip=clip)
        return pix.tobytes()  # return the PNG image
