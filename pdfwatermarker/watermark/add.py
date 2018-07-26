# Add a watermark PDF file to another PDF file
import os
from pdfrw import PdfReader, PdfWriter, PageMerge
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.pagesizes import letter
from pdfwatermarker import upscale, rotate, add_suffix


def get_pdf_size(file_name):
    """Get width and height of a PDF"""
    try:
        size = PdfFileReader(file_name).getPage(0).mediaBox
    except AttributeError:
        size = file_name.getPage(0).mediaBox
    return {'w': size[2], 'h': size[3]}


class WatermarkAdd:
    def __init__(self, document, watermark, underneath=False, decrypt=False):
        self.rotate = 0
        self.document_reader = self._document_reader(document, decrypt)
        self.document = self._get_pdf_info(document)
        self.watermark_file = self._get_watermark_info(self.document, watermark)
        pdf_fname, wtrmrk_fname = self._set_filenames
        self.output = self.add(pdf_fname, wtrmrk_fname, underneath)

    def __str__(self):
        return str(self.output)

    @staticmethod
    def _document_reader(document, decrypt=False):
        if decrypt:
            reader = PdfFileReader(document)
            reader.decrypt(decrypt)
            return reader
        else:
            return PdfFileReader(document)

    def _get_pdf_info(self, filename):
        pdf_file = {'path': filename}

        # Get PDF width and height
        pdf_file.update(get_pdf_size(self.document_reader))

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
            self.document_reader = self._document_reader(pdf_file['upscaled'])
        return pdf_file

    def _get_watermark_info(self, document, watermark):
        watermark_file = {'path': watermark}
        watermark_file.update(get_pdf_size(watermark))

        # Check if watermark file needs to be rotated
        if watermark_file['w'] > watermark_file['h'] and document['orientation'] is 'vertical':
            self.rotate = 90
            watermark_file['rotated'] = rotate(watermark, 90)
        return watermark_file

    @property
    def _set_filenames(self):
        # If upscaled PDF file does not exists use input PDF path
        try:
            pdf = self.document['upscaled']
        except KeyError:
            pdf = self.document['path']

        # If rotated watermark file does not exists use input watermark path
        try:
            watermark = self.watermark_file['rotated']
        except KeyError:
            watermark = self.watermark_file['path']
        return pdf, watermark

    def add(self, document, watermark, underneath=False, method='pypdf2'):
        """Add watermark to PDF by merging original PDF and watermark file."""
        output_filename = add_suffix(self.document['path'], 'watermarked')

        def pypdf2():
            # Get our files ready
            watermark_reader = PdfFileReader(watermark)
            document_reader = self.document_reader
            output_file = PdfFileWriter()

            # Number of pages in input document
            page_count = document_reader.getNumPages()

            # Go through all the input file pages to add a watermark to them
            for page_number in range(page_count):
                # Merge the watermark with the page
                input_page = document_reader.getPage(page_number)
                wtrmrk_page = watermark_reader.getPage(0)
                input_page.mergeRotatedTranslatedPage(wtrmrk_page, self.rotate,
                                                      wtrmrk_page.mediaBox.getWidth() / 2,
                                                      wtrmrk_page.mediaBox.getWidth() / 2)

                # Add page from input file to output document
                output_file.addPage(input_page)

            # finally, write "output" to PDF
            with open(output_filename, "wb") as outputStream:
                output_file.write(outputStream)
            return output_filename

        def pdfrw():
            wmark = PageMerge().add(PdfReader(watermark).pages[0])[0]

            trailer = PdfReader(document)
            for page in trailer.pages:
                PageMerge(page).add(wmark, prepend=underneath).render()

            PdfWriter(output_filename, trailer=trailer).write()
            return output_filename

        if method is 'pypdf2':
            return pypdf2()
        else:
            return pdfrw()
