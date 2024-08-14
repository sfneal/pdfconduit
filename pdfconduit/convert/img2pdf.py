# Convert a PNG image file to a PDF
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional, List, Union

from PIL import Image

from pdfconduit.transform.merge import Merge
from pdfconduit.watermark.modify.canvas import CanvasImg, CanvasObjects
from pdfconduit.watermark.modify.draw import WatermarkDraw


class IMG2PDF:
    def __init__(
        self,
        imgs: Optional[List[str]] = None,
        destination: Optional[str] = None,
        tempdir: Optional[Union[str, TemporaryDirectory]] = None,
    ):
        """Convert each image into a PDF page and merge all pages to one PDF file"""
        self.imgs = imgs
        self.output_dir = destination
        if not tempdir:
            self._temp = TemporaryDirectory()
            self.tempdir = self._temp.name
        elif isinstance(tempdir, TemporaryDirectory):
            self._temp = tempdir
            self.tempdir = self._temp.name
        else:
            self.tempdir = tempdir

        self._pdf_pages = None

    @property
    def pdf_pages(self) -> List[str]:
        if not self._pdf_pages:
            self._pdf_pages = self.img2pdf()
        return self._pdf_pages

    def cleanup(self, clean_temp: bool = True) -> None:
        if clean_temp and hasattr(self, "_temp"):
            self._temp.cleanup()

    def _image_loop(self) -> List[str]:
        """Retrieve an iterable of images either with, or without a progress bar."""
        return self.imgs

    def _convert(self, image, output: Optional[str] = None) -> str:
        """Private method for converting a single PNG image to a PDF."""
        with Image.open(image) as im:
            width, height = im.size

            co = CanvasObjects()
            co.add(CanvasImg(image, 1.0, w=width, h=height, mask=None))

            return WatermarkDraw(
                co, tempdir=self.tempdir, pagesize=(width, height)
            ).write(output)

    def convert(self, image: str, output: Optional[str] = None):
        """
        Convert an image to a PDF.

        :param image: Image file path
        :param output: Output name, same as image name with .pdf extension by default
        :return: PDF file path
        """
        return self._convert(
            image, image.replace(Path(image).suffix, ".pdf") if not output else output
        )

    def img2pdf(self) -> List[str]:
        """Convert a list of images into a PDF files."""
        return [self._convert(image) for image in self._image_loop()]

    def save(self, output_name: str = "merged imgs", clean_temp: bool = True) -> str:
        m = Merge(self.pdf_pages, output_name=output_name, output_dir=self.output_dir)
        self.cleanup(clean_temp)
        return m.merge()
