# Create flat PDF by converting each input PDF page to a PNG
import os
from tempfile import TemporaryDirectory
from typing import List, Optional

from pdfconduit.convert.img2pdf import IMG2PDF
from pdfconduit.convert.pdf2img import PDF2IMG
from pdfconduit.transform.upscale import Upscale
from pdfconduit.utils.path import add_suffix


class Flatten:
    def __init__(
        self,
        file_name: str,
        scale: float = 1.0,
        suffix: str = "flat",
        tempdir: Optional[str] = None,
    ):
        """Create a flat single-layer PDF by converting each page to a PNG image"""
        self._file_name = file_name

        if not tempdir:
            self._temp = TemporaryDirectory()
            self.tempdir = self._temp.name
        elif isinstance(tempdir, TemporaryDirectory):
            self._temp = tempdir
            self.tempdir = self._temp.name
        else:
            self._temp = None
            self.tempdir = tempdir

        self.suffix = suffix
        self.directory = os.path.dirname(file_name)

        if scale and scale != 0 and scale != 1.0:
            self.file_name = Upscale(
                file_name, scale=scale, tempdir=self.tempdir
            ).upscale()
        else:
            self.file_name = self._file_name

        self.imgs = None
        self.pdf = None

    def __str__(self) -> str:
        return str(self.pdf)

    def get_imgs(self) -> List[str]:
        self.imgs = PDF2IMG(self.file_name, output_directory=self.tempdir).convert()
        return self.imgs

    def save(self, remove_temps: bool = True) -> str:
        if self.imgs is None:
            self.get_imgs()
        i2p = IMG2PDF(self.imgs, add_suffix(self._file_name, self.suffix), self._temp)
        self.pdf = i2p.convert()
        if remove_temps:
            self.cleanup(remove_temps)
        return self.pdf

    def cleanup(self, clean_temp: bool = True) -> None:
        if clean_temp and self._temp:
            self._temp.cleanup()
