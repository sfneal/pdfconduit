# Create flat PDF by converting each input PDF page to a PNG
import os
from tempfile import TemporaryDirectory

from pdf.convert.img2pdf import IMG2PDF
from pdf.convert.pdf2img import PDF2IMG
from pdf.transform.upscale import upscale
from pdf.utils.path import add_suffix


class Flatten:
    def __init__(self, file_name, scale=1.0, suffix='flat', tempdir=None, progress_bar=None):
        """Create a flat single-layer PDF by converting each page to a PNG image"""
        self._file_name = file_name

        if not tempdir:
            self._temp = TemporaryDirectory()
            self.tempdir = self._temp.name
        elif isinstance(tempdir, TemporaryDirectory):
            self._temp = tempdir
            self.tempdir = self._temp.name
        else:
            self.tempdir = tempdir

        self.suffix = suffix
        self.directory = os.path.dirname(file_name)
        self.progress_bar = progress_bar

        if scale and scale is not 0 and scale is not 1.0:
            self.file_name = upscale(file_name, scale=scale, tempdir=self.tempdir)
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
        self.pdf = i2p.save(clean_temp=False, output_name=add_suffix(self._file_name, self.suffix))
        self.cleanup(remove_temps)
        return self.pdf

    def cleanup(self, clean_temp=True):
        if clean_temp and hasattr(self, '_temp'):
            self._temp.cleanup()
