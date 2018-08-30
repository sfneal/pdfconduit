# Create flat PDF by converting each input PDF page to a PNG
import os
from tempfile import mkdtemp
from pdf.utils.path import add_suffix
from pdf.conduit.upscale import upscale
from pdf.conduit.convert.img2pdf import IMG2PDF
from pdf.conduit.convert.pdf2img import PDF2IMG


class Flatten:
    def __init__(self, file_name, scale=2.0, suffix='flat', tempdir=None, progress_bar=None):
        """Create a flat single-layer PDF by converting each page to a PNG image"""
        self._file_name = file_name
        self.tempdir = tempdir if tempdir else mkdtemp()
        self.suffix = suffix
        self.directory = os.path.dirname(file_name)
        self.progress_bar = progress_bar

        if scale and scale is not 0 and scale is not 1.0:
            self.file_name = upscale(file_name, scale=scale, tempdir=tempdir)
        else:
            self.file_name = self._file_name

        self.imgs = None
        self.pdf = None

    def __str__(self):
        return str(self.pdf)

    def get_imgs(self):
        self.imgs = PDF2IMG(self.file_name, tempdir=self.tempdir, progress_bar=self.progress_bar).save()
        return self.imgs

    def save(self, remove_temps=True):
        if self.imgs is None:
            self.get_imgs()
        i2p = IMG2PDF(self.imgs, self.directory, self.tempdir, self.progress_bar)
        self.pdf = i2p.save(remove_temps=remove_temps, output_name=add_suffix(self._file_name, self.suffix))
        return self.pdf
