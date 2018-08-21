import os
import fitz
from io import BytesIO
from PIL import Image
from pdfconduit.utils import add_suffix
from pdfconduit.watermark.canvas.objects import CanvasImg, CanvasObjects
from pdfconduit.watermark.draw.pdf import WatermarkDraw
from pdfconduit.merge import Merge


class PDFtoIMG:
    def __init__(self, file_name, tempdir=None, ext='png'):
        self.file_name = file_name
        self.doc = fitz.open(self.file_name)
        self.ext = ext
        self.output_dir = os.path.dirname(file_name) if tempdir is None else tempdir

        # storage for page display lists
        self.dlist_tab = [None] * len(self.doc)
        self.pdf_data = self.get_pdf_data()

    def save_imgs(self):
        saved = []
        for i, img in enumerate(self.pdf_data):
            output_file = add_suffix(self.file_name, str(i), ext=self.ext)
            image = Image.open(BytesIO(img))
            output = os.path.join(self.output_dir, output_file)
            image.save(output)
            saved.append(output)
        return saved

    def get_pdf_data(self):
        return [self.get_page_data(cur_page) for cur_page in range(len(self.doc))]

    def get_page_data(self, pno, zoom=0):
        """
        Return a PNG image for a document page number. If zoom is other than 0, one of
        the 4 page quadrants are zoomed-in instead and the corresponding clip returned.
        """
        dlist = self.dlist_tab[pno]  # get display list
        if not dlist:  # create if not yet there
            self.dlist_tab[pno] = self.doc[pno].getDisplayList()
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
            pix = dlist.getPixmap(alpha=False)
        else:
            pix = dlist.getPixmap(alpha=False, matrix=mat, clip=clip)
        return pix.getPNGData()  # return the PNG image


def main():
    directory = '/Users/Stephen/Dropbox/scripts/pdfconduit/tests/data'
    fname = os.path.join(directory, 'con docs2.pdf')
    imgs = PDFtoIMG(fname).save_imgs()
    pdfs = []

    for i in imgs:
        co = CanvasObjects()
        co.add(CanvasImg(i, 1.0))
        pdf = WatermarkDraw(co).write()
        pdfs.append(pdf)

    Merge(pdfs, output_dir=directory)


if __name__ == '__main__':
    main()
