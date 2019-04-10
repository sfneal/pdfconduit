# Convert a PNG image file to a PDF
from sys import modules
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

    def img2pdf(self):
        # TODO: Figure out weather this method is causing unclosed file warnings and errors
        # PySimpleGUI progress bar
        if self.progress_bar is 'gui' and 'PySimpleGUI' in modules:
            import PySimpleGUI as sg
            pdfs = []
            for index, i in enumerate(self.imgs):
                with Image.open(i) as im:
                    width, height = im.size

                    co = CanvasObjects()
                    co.add(CanvasImg(i, 1.0, w=width, h=height))

                    pdf = WatermarkDraw(co, tempdir=self.tempdir, pagesize=(width, height)).write()
                    pdfs.append(pdf)
                if not sg.OneLineProgressMeter('Saving PNGs as flat PDFs', index + 1, len(self.imgs),
                                               orientation='h', key='progress'):
                    break
            return pdfs

        # TQDM progress bar
        elif self.progress_bar is 'tqdm':
            loop = tqdm(self.imgs, desc='Saving PNGs as flat PDFs', total=len(self.imgs), unit='PDFs')

        # No progress bar
        else:
            loop = self.imgs
        pdfs = []
        for i in loop:
            with Image.open(i) as im:
                width, height = im.size

            co = CanvasObjects()
            co.add(CanvasImg(i, 1.0, w=width, h=height))

            pdf = WatermarkDraw(co, tempdir=self.tempdir, pagesize=(width, height)).write()
            pdfs.append(pdf)
        return pdfs

    def save(self, output_name='merged imgs'):
        m = str(Merge(self.pdf_pages, output_name=output_name, output_dir=self.output_dir))
        if hasattr(self, '_temp'):
            self._temp.cleanup()
        return m


def img2pdf(imgs, output_name='merged_imgs', destination=None, tempdir=None, progress_bar=None):
    return IMG2PDF(imgs, destination, tempdir, progress_bar).save(output_name)
