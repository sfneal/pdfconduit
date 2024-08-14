# Convert each page of PDF to images
import os
from io import BytesIO
from tempfile import NamedTemporaryFile
from typing import Optional, List

import fitz
from PIL import Image

from pdfconduit.utils.path import add_suffix


class PDF2IMG:
    def __init__(
        self,
        file_name: str,
        output: Optional[str] = None,
        tempdir: Optional[str] = None,
        ext: str = ".png",
        alpha: bool = False,
    ):
        """Convert each page of a PDF file into a PNG image"""
        self.file_name = file_name
        self.output = output
        self.tempdir = tempdir
        self.ext = ext
        self.alpha = alpha

        self.doc = fitz.open(self.file_name)
        self.output_dir = os.path.dirname(file_name) if tempdir is None else tempdir

        # storage for page display lists
        self.dlist_tab = [None] * len(self.doc)
        self._page_data = None

    @property
    def pdf_data(self) -> List[bytes]:
        if not self._page_data:
            self._page_data = self._get_pdf_data()
        return self._page_data

    def _get_pdf_data(self) -> List[bytes]:
        return [self._get_page_data(cur_page) for cur_page in range(len(self.doc))]

    def _get_page_data(self, pno, zoom=0) -> bytes:
        """
        Return a PNG image for a document page number. If zoom is other than 0, one of
        the 4 page quadrants are zoomed-in instead and the corresponding clip returned.
        """
        dlist = self.dlist_tab[pno]  # get display list
        if not dlist:  # create if not yet there
            self.dlist_tab[pno] = self.doc[pno].get_displaylist()
            dlist = self.dlist_tab[pno]
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
            pix = dlist.get_pixmap(alpha=self.alpha)
        else:
            pix = dlist.get_pixmap(alpha=self.alpha, matrix=mat, clip=clip)
        return pix.tobytes()  # return the PNG image

    def _get_output(self, index: int) -> str:
        if self.output:
            return self.output
        elif not self.tempdir:
            output_file = add_suffix(self.file_name, str(index + 1), ext=self.ext)
            return os.path.join(self.output_dir, output_file)
        else:
            with NamedTemporaryFile(
                suffix=self.ext, dir=self.tempdir, delete=True
            ) as temp:
                return temp.name

    def save(self) -> List[str]:
        saved = []
        for i, img in enumerate(self.pdf_data):
            output = self._get_output(i)
            saved.append(output)
            with Image.open(BytesIO(img)) as image:
                image.save(output)
        self.doc.close()
        return saved
