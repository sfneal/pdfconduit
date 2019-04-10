# Convert a PNG image file to a PDF
from PIL import Image
from tqdm import tqdm
from tempfile import TemporaryDirectory

from pdf.modify.canvas import CanvasImg, CanvasObjects
from pdf.modify.draw import WatermarkDraw
from pdf.transform.merge import Merge


class IMG2PDF:
    def __init__(self, imgs, destination=None, tempdir=None, progress_bar=None):
        """Convert each image into a PDF page and merge all pages to one PDF file"""
        self.imgs = imgs
        self.output_dir = destination
        if not tempdir:
            self._temp = TemporaryDirectory()
            self.tempdir = self._temp.name
        self.progress_bar = progress_bar

        self.pdf_pages = self.img2pdf()

    def _image_loop(self):
        """Retrieve an iterable of images either with, or without a progress bar."""
        if self.progress_bar and 'tqdm' in self.progress_bar.lower():
            return tqdm(self.imgs, desc='Saving PNGs as flat PDFs', total=len(self.imgs), unit='PDFs')
        else:
            return self.imgs

    def convert(self, image):
        """Convert a single PNG image to a PDF."""
        with Image.open(image) as im:
            width, height = im.size

            co = CanvasObjects()
            co.add(CanvasImg(image, 1.0, w=width, h=height))

            return WatermarkDraw(co, tempdir=self.tempdir, pagesize=(width, height)).write()

    def img2pdf(self):
        """Convert a list of images into a PDF files."""
        return [self.convert(image) for image in self._image_loop()]

    def save(self, output_name='merged imgs', clean_temp=True):
        m = str(Merge(self.pdf_pages, output_name=output_name, output_dir=self.output_dir))
        if clean_temp and hasattr(self, '_temp'):
            self._temp.cleanup()
        return m


def img2pdf(imgs, output_name='merged_imgs', destination=None, tempdir=None, progress_bar=None):
    return IMG2PDF(imgs, destination, tempdir, progress_bar).save(output_name)
