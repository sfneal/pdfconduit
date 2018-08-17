# Add a watermark PDF file to another PDF file
from tempfile import NamedTemporaryFile
from pdfrw import PdfReader, PdfWriter, PageMerge
from PyPDF3 import PdfFileReader, PdfFileWriter
from reportlab.lib.pagesizes import letter
from pdfconduit.upscale import upscale
from pdfconduit.rotate import rotate
from pdfconduit.utils import add_suffix, resource_path, Info


class WatermarkAdd:
    def __init__(self, document, watermark, underneath=False, overwrite=False, output=None, suffix='watermarked',
                 decrypt=False, tempdir=None):
        """
        Add a watermark to an existing PDF document

        1. Read PDF document and decrypt if encrypted
        2. Get input PDF document info
            2a. Retrieve dimensions
            2b. Determine orientation
            2c. Upscale to fit letter
        3. Get watermark info
            3a. Retrieve dimensions
            3b. Rotate if necessary
            3c. Upscale to fit document
        4. Set file names
            4a. Check if a upscaled doc was created, if not use original document
            4b. Check if watermark was rotated, if not use original watermark
        5. Add watermark to PDF document
            5a. Create watermarked document filename (ex: originalpdfname_watermarked.pdf)
            5b. Create PDF file reader and file writer objects
            5c. Add watermark to each page of original
            5d. Save watermarked document to file
        """
        self.rotate = 0
        self.scale = 0
        self.tempdir = tempdir
        self.document_reader = self._document_reader(document, decrypt)
        self.document = self._get_document_info(document)
        self.watermark_file = self._get_watermark_info(self.document, watermark)
        pdf_fname, wtrmrk_fname = self._set_filenames

        if overwrite:
            self.output_filename = document
        elif output:
            if output == 'temp':
                tmpf = NamedTemporaryFile(suffix='.pdf', dir=self.tempdir, delete=False)
                self.output_filename = resource_path(tmpf.name)
            else:
                self.output_filename = output
        else:
            self.output_filename = add_suffix(document, suffix)

        self.add(pdf_fname, wtrmrk_fname, underneath)

    def __str__(self):
        return str(self.output_filename)

    @staticmethod
    def _document_reader(document, decrypt=False):
        # 1. Read PDF document and create file reader object
        if decrypt:
            reader = PdfFileReader(document)
            reader.decrypt(decrypt)
            return reader
        else:
            return PdfFileReader(document)

    def _get_document_info(self, filename):
        pdf_file = {'path': filename}

        # 2a. Get PDF width and height
        pdf_file.update(Info(self.document_reader).dimensions)

        # 2b. Get PDF file orientation
        if pdf_file['h'] > pdf_file['w']:
            pdf_file['orientation'] = 'portrait'
            letter_size = {'w': int(letter[0]), 'h': int(letter[1])}
        else:
            pdf_file['orientation'] = 'landscape'
            letter_size = {'h': int(letter[0]), 'w': int(letter[1])}

        # 2c. Upscale PDF if it is smaller than a letter
        if pdf_file['w'] <= letter_size['w'] or pdf_file['h'] <= letter_size['h']:
            scale = float(letter_size['w'] / pdf_file['w'])
            pdf_file['upscaled'] = upscale(pdf_file['path'], scale=scale, tempdir=self.tempdir)
            self.document_reader = self._document_reader(pdf_file['upscaled'])
        return pdf_file

    def _get_watermark_info(self, document, watermark, margin_x=0, margin_y=0):
        # 3a. Get watermark path and dimensions
        watermark_file = {'path': watermark}
        watermark_file.update(Info(watermark).dimensions)

        # 3b. Check if watermark file needs to be rotated
        if watermark_file['w'] > watermark_file['h'] and document['orientation'] is 'portrait':
            self.rotate = 90
            watermark_file['rotated'] = rotate(watermark, self.rotate, tempdir=self.tempdir)

        # Set watermark file to be used for upscaling
        try:
            wtrmrk = watermark_file['rotated']
            watermark_file.update(Info(watermark_file['rotated']).dimensions)
        except KeyError:
            wtrmrk = watermark_file['path']

        # 3c. Check if watermark file needs to be upscaled
        scale = 0
        if watermark_file['w'] <= document['w']:
            scale = float(document['w'] / watermark_file['w'])

            if watermark_file['h'] * scale > document['h']:
                scale = float(document['h'] / watermark_file['h'])

            if watermark_file['w'] * scale < document['w']:
                margin_x = (document['w'] - watermark_file['w'] * scale) / 2
            watermark_file['upscaled'] = upscale(wtrmrk, margin_x=margin_x, scale=scale, tempdir=self.tempdir)
        self.scale = scale
        return watermark_file

    @property
    def _set_filenames(self):
        # 4a. If upscaled PDF file does not exists use input PDF path
        try:
            pdf = self.document['upscaled']
        except KeyError:
            pdf = self.document['path']

        # 4b. If rotated watermark file does not exists use input watermark path
        try:
            try:
                watermark = self.watermark_file['upscaled']
            except KeyError:
                watermark = self.watermark_file['rotated']
        except KeyError:
            watermark = self.watermark_file['path']
        return pdf, watermark

    def add(self, document, watermark, underneath=False, method='pypdf2'):
        """Add watermark to PDF by merging original PDF and watermark file."""
        # 5a. Create output PDF file name
        output_filename = self.output_filename

        def pypdf2():
            # TODO: Fix functionality
            # 5b. Get our files ready
            document_reader = self.document_reader
            output_file = PdfFileWriter()

            # Number of pages in input document
            page_count = document_reader.getNumPages()

            # Watermark objects
            watermark_reader = PdfFileReader(watermark)
            wtrmrk_page = watermark_reader.getPage(0)
            wtrmrk_width = wtrmrk_page.mediaBox.getWidth() / 2
            wtrmrk_height = wtrmrk_page.mediaBox.getHeight() / 2
            wtrmrk_rotate = Info(watermark_reader).rotate
            print(wtrmrk_width, wtrmrk_height)
            print(watermark)
            print(Info(watermark_reader).size)
            print(wtrmrk_rotate)

            # 5c. Go through all the input file pages to add a watermark to them
            for page_number in range(page_count):
                # Merge the watermark with the page
                input_page = document_reader.getPage(page_number)
                input_page.mergeRotatedTranslatedPage(wtrmrk_page, -wtrmrk_rotate, wtrmrk_width, wtrmrk_height)

                # Add page from input file to output document
                output_file.addPage(input_page)

            # 5d. finally, write "output" to PDF
            with open(output_filename, "wb") as outputStream:
                output_file.write(outputStream)
            return output_filename

        def pdfrw():
            # 5b. Get watermark from reader
            wmark = PageMerge().add(PdfReader(watermark).pages[0])[0]

            # 5c. Add watermark to each page of document
            trailer = PdfReader(document)
            for page in trailer.pages:
                PageMerge(page).add(wmark, prepend=underneath).render()

            # 5d. Write PDF to file
            PdfWriter(output_filename, trailer=trailer).write()
            return output_filename

        if method is 'pypdf2':
            return pypdf2()
        else:
            return pdfrw()
