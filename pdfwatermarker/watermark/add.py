# Add a watermark PDF file to another PDF file
import os
from pdfrw import PdfReader, PdfWriter, PageMerge
from PyPDF2 import PdfFileReader
from reportlab.lib.pagesizes import letter
from pdfwatermarker import upscale, rotate, add_suffix


def get_pdf_size(file_name):
    """Get width and height of a PDF"""
    f = open(file_name, 'rb')
    input1 = PdfFileReader(f)
    size = input1.getPage(0).mediaBox
    f.close()
    return {'w': size[2], 'h': size[3]}


class WatermarkAdd:
    def __init__(self, pdf, watermark, underneath=False):
        self.pdf_file = self._get_pdf_info(pdf)
        self.watermark_file = self._get_watermark_info(watermark)
        pdf_fname, wtrmrk_fname = self._set_filenames
        self.output = self.add(pdf_fname, wtrmrk_fname, underneath)

    def __str__(self):
        return str(self.output)

    @staticmethod
    def _get_pdf_info(filename):
        pdf_file = {'path': filename}

        # Get PDF width and height
        pdf_file.update(get_pdf_size(pdf_file['path']))

        # Get PDF file orientation
        if pdf_file['h'] > pdf_file['w']:
            pdf_file['orientation'] = 'vertical'
            letter_size = {'w': int(letter[0]), 'h': int(letter[1])}
        else:
            pdf_file['orientation'] = 'horizontal'
            letter_size = {'h': int(letter[0]), 'w': int(letter[1])}

        # Upscale PDF if it is smaller than a letter
        if pdf_file['w'] != letter_size['w'] or pdf_file['h'] != letter_size['h']:
            scale = float(letter_size['w'] / pdf_file['w'])
            pdf_file['upscaled'] = upscale(pdf_file['path'], scale=scale)
        return pdf_file

    def _get_watermark_info(self, watermark):
        watermark_file = {'path': watermark}
        watermark_file.update(get_pdf_size(watermark))

        # Check if watermark file needs to be rotated
        if watermark_file['w'] > watermark_file['h'] and self.pdf_file['orientation'] is 'vertical':
            watermark_file['rotated'] = rotate(watermark, 90)
        return watermark_file

    @property
    def _set_filenames(self):
        # If upscaled PDF file does not exists use input PDF path
        try:
            pdf = self.pdf_file['upscaled']
        except KeyError:
            pdf = self.pdf_file['path']

        # If rotated watermark file does not exists use input watermark path
        try:
            watermark = self.watermark_file['rotated']
        except KeyError:
            watermark = self.watermark_file['path']
        return pdf, watermark

    def add(self, filename, watermark, underneath=False):
        """Add watermark to PDF by merging original PDF and watermark file."""
        outfn = add_suffix(self.pdf_file['path'], '_watermarked')

        wmark = PageMerge().add(PdfReader(watermark).pages[0])[0]

        trailer = PdfReader(filename)
        for page in trailer.pages:
            PageMerge(page).add(wmark, prepend=underneath).render()

        PdfWriter(outfn, trailer=trailer).write()
        return outfn
