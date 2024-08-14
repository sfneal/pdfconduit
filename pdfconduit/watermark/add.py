# Add a watermark PDF file to another PDF file
from tempfile import NamedTemporaryFile
from typing import Optional, Tuple

from PyBundle import resource_path
from pdfrw import PdfReader, PdfWriter, PageMerge
from pypdf import PdfReader as PypdfReader, PdfWriter as PypdfWriter
from reportlab.lib.pagesizes import letter

from pdfconduit.transform import Rotate, Upscale
from pdfconduit.utils import add_suffix, Info, pypdf_reader
from pdfconduit.utils.driver import PdfDriver


class WatermarkAdd(PdfDriver):
    def __init__(
        self,
        document: str,
        watermark: str,
        underneath: bool = False,
        overwrite: bool = False,
        output: Optional[str] = None,
        suffix: Optional[str] = "watermarked",
        decrypt: bool = False,
        tempdir: Optional[str] = None,
    ):
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
        self.underneath = underneath
        self.tempdir = tempdir

        self.document_reader = pypdf_reader(document, decrypt)
        self.document = self._get_document_info(document)
        self.watermark_file = self._get_watermark_info(self.document, watermark)
        self.pdf_fname, self.wtrmrk_fname = self._set_filenames

        if overwrite:
            self.output_filename = document
        elif output:
            self.output_filename = output
        elif suffix:
            self.output_filename = add_suffix(document, suffix)
        else:
            tmpf = NamedTemporaryFile(suffix=".pdf", dir=self.tempdir, delete=False)
            self.output_filename = resource_path(tmpf.name)

    def __str__(self):
        return str(self.output_filename)

    def _get_document_info(self, filename: str) -> dict:
        # todo: add use of typed dictionary
        pdf_file = {"path": filename}

        # 2a. Get PDF width and height
        # todo: optimize so that a pdf reader can be passed
        pdf_file.update(Info(filename).dimensions)

        # 2b. Get PDF file orientation
        if pdf_file["h"] > pdf_file["w"]:
            pdf_file["orientation"] = "portrait"
            letter_size = {"w": int(letter[0]), "h": int(letter[1])}
        else:
            pdf_file["orientation"] = "landscape"
            letter_size = {"h": int(letter[0]), "w": int(letter[1])}

        # 2c. Upscale PDF if it is smaller than a letter
        if pdf_file["w"] <= letter_size["w"] or pdf_file["h"] <= letter_size["h"]:
            scale = float(letter_size["w"] / pdf_file["w"])
            # todo: add use of upscale class instead of function
            pdf_file["upscaled"] = (
                Upscale(pdf_file["path"], scale=scale, tempdir=self.tempdir)
                .use(self._driver)
                .upscale()
            )
            self.document_reader = pypdf_reader(pdf_file["upscaled"])
        return pdf_file

    def _get_watermark_info(
        self, document: dict, watermark: str, margin_x: int = 0, margin_y: int = 0
    ) -> dict:
        # todo: add use of typed dictionary
        # 3a. Get watermark path and dimensions
        watermark_file = {"path": watermark}
        watermark_file.update(Info(watermark).dimensions)

        # 3b. Check if watermark file needs to be rotated
        if (
            watermark_file["w"] > watermark_file["h"]
            and document["orientation"] == "portrait"
        ):
            self.rotate = 90
            watermark_file["rotated"] = (
                Rotate(watermark, self.rotate, tempdir=self.tempdir)
                .use(self._driver)
                .rotate()
            )

        # Set watermark file to be used for upscaling
        try:
            wtrmrk = watermark_file["rotated"]
            watermark_file.update(Info(watermark_file["rotated"]).dimensions)
        except KeyError:
            wtrmrk = watermark_file["path"]

        # 3c. Check if watermark file needs to be upscaled
        scale = 0
        if watermark_file["w"] <= document["w"]:
            scale = float(document["w"] / watermark_file["w"])

            if watermark_file["h"] * scale > document["h"]:
                scale = float(document["h"] / watermark_file["h"])

            watermark_file["upscaled"] = (
                Upscale(wtrmrk, scale=scale, tempdir=self.tempdir)
                .use(self._driver)
                .upscale()
            )
        self.scale = scale
        return watermark_file

    @property
    def _set_filenames(self) -> Tuple[str, str]:
        # 4a. If upscaled PDF file does not exist use input PDF path
        try:
            pdf = self.document["upscaled"]
        except KeyError:
            pdf = self.document["path"]

        # 4b. If rotated watermark file does not exist use input watermark path
        try:
            try:
                watermark = self.watermark_file["upscaled"]
            except KeyError:
                watermark = self.watermark_file["rotated"]
        except KeyError:
            watermark = self.watermark_file["path"]
        return pdf, watermark

    def add(self) -> str:
        """Add watermark to PDF by merging original PDF and watermark file."""
        return self.execute()

    def pypdf(self) -> str:
        watermark_page = PypdfReader(self.wtrmrk_fname).get_page(0)

        writer = PypdfWriter()

        reader = PypdfReader(self.pdf_fname)
        writer.append(reader)

        # width = float(watermark_page.mediabox[2]) / 2
        # height = float(watermark_page.mediabox[3]) / 2

        for content_page in writer.pages:
            # content_page.merge_translated_page(watermark_page, tx=width, ty=height, over=False)
            content_page.merge_page(watermark_page, over=False)

        with open(self.output_filename, "wb") as fp:
            writer.write(fp)

        return self.output_filename

    def pdfrw(self) -> str:
        """Faster than PyPDF3 method by as much as 15x."""
        # TODO: Fix issue where watermark is improperly placed on large pagesize PDFs
        # print(Info(document).size)
        # print(Info(watermark).size)
        # print('\n')

        # Open both the source files
        wmark_trailer = PdfReader(self.wtrmrk_fname)
        trailer = PdfReader(self.pdf_fname)

        # Handle different sized pages in same document with
        # a memoization cache, so we don't create more watermark
        # objects than we need to (typically only one per document).

        wmark_page = wmark_trailer.pages[0]
        wmark_cache = {}

        # Process every page
        for pagenum, page in enumerate(trailer.pages, 1):

            # Get the media box of the page, and see
            # if we have a matching watermark in the cache
            mbox = tuple(float(x) for x in page.MediaBox)
            odd = pagenum & 1
            key = mbox, odd
            wmark = wmark_cache.get(key)
            if wmark is None:

                # Create and cache a new watermark object.
                wmark = wmark_cache[key] = PageMerge().add(wmark_page)[0]

                # The math is more complete than it probably needs to be,
                # because the origin of all pages is almost always (0, 0).
                # Nonetheless, we illustrate all the values and their names.

                page_x, page_y, page_x1, page_y1 = mbox
                page_w = page_x1 - page_x
                page_h = page_y1 - page_y  # For illustration, not used

                # Scale the watermark if it is too wide for the page
                # (Could do the same for height instead if needed)
                if wmark.w > page_w:
                    wmark.scale(1.0 * page_w / wmark.w)

                # Always put watermark at the top of the page
                # (but see horizontal positioning for other ideas)
                wmark.y += page_y1 - wmark.h

                # For odd pages, put it at the left of the page,
                # and for even pages, put it on the right of the page.
                if odd:
                    wmark.x = page_x
                else:
                    wmark.x += page_x1 - wmark.w

                # Optimize the case where the watermark is same width
                # as page.
                if page_w == wmark.w:
                    wmark_cache[mbox, not odd] = wmark

            # Add the watermark to the page
            PageMerge(page).add(wmark, prepend=self.underneath).render()

        # Write out the destination file
        PdfWriter(self.output_filename, trailer=trailer).write()
        return self.output_filename
