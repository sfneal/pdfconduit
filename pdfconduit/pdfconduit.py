from pypdf import PdfWriter

from pdfconduit.convert import Flatten
from pdfconduit.internals import BaseConduit
from pdfconduit.settings import Compression, ImageQualityRange, Encryption
from pdfconduit.transform import Merge2, Scale
from pdfconduit.transform import Rotate
from pdfconduit.utils import Info
from pdfconduit.utils.typing import Optional, Tuple, Self, Annotated


class Pdfconduit(BaseConduit):
    def encrypt(self, encrypter: Encryption) -> Self:
        self._set_default_output("encrypted")
        self._writer.encrypt(
            user_password=encrypter.user_pw,
            owner_password=encrypter.owner_pw,
            permissions_flag=encrypter.permissions,
            algorithm=encrypter.algo.value,
        )
        return self

    def merge(self, pdf: str, position: Optional[int] = None) -> Self:
        # todo: allow for iterable of pdfs
        self._set_default_output("merged")
        if position is None:
            self._writer.append(pdf)
        else:
            self._writer.merge(position, pdf)
        return self

    def merge_fast(self, pdfs: list) -> Self:
        self._set_default_output("merged")
        # todo: extract method for stream or path
        pdf_objects = [self.pdf_object] + pdfs
        self._path = Merge2(pdf_objects, output=self.output).use_pdfrw().merge()
        return self._open_and_read()

    def rotate(self, degrees: int) -> Self:
        self._set_default_output("rotated")
        for page in self._writer.pages:
            page.rotate(degrees)
        return self

    def rotate_exact(self, degrees: int) -> Self:
        if degrees % 90 == 0:
            return self.rotate(degrees)

        self._set_default_output("rotated")
        self._path = (
            Rotate(
                self.pdf_object,
                degrees,
                output=self.output,
            )
            .use_pdfrw()
            .rotate()
        )
        return self._open_and_read()

    def slice(self, start: int, end: int) -> Self:
        self._set_default_output("sliced")
        start = start - 1  # Reindex page selections for simple user input
        writer = PdfWriter()
        for page_num in list(range(self._writer.get_num_pages()))[start:end]:
            writer.add_page(self._writer.get_page(page_num))
        self._writer = writer
        return self

    def scale(
        self, scale: float, margins: Tuple[int, int] = (0, 0), accelerate: bool = False
    ) -> Self:
        self._set_default_output("scaled")

        if accelerate or margins != (0, 0):
            x, y = margins
            self._path = (
                Scale(
                    self.pdf_object,
                    output=self.output,
                    scale=scale,
                    margin_x=x,
                    margin_y=y,
                )
                .use_pdfrw()
                .execute()
            )
            return self._open_and_read()

        width, height = self.info.size
        width, height = (width * scale, height * scale)
        for page in self._writer.pages:
            page.scale_to(width, height)
        return self

    def flatten(self) -> Self:
        # todo: re-write Flatten & other convert classes
        # todo: fix issue with flattened pdf output path
        if not self._closed:
            self.write()

        self._path = Flatten(
            self.output, suffix="flattened", tempdir=self._output_dir
        ).save()

        return self._open_and_read()

    def minify(self) -> Self:
        # remove duplication (images or pages) from a PDF
        self._set_default_output("minified")
        writer = PdfWriter()
        for page in self._writer.pages:
            writer.add_page(page)
        self._writer = writer
        return self

    def remove_duplication(self) -> Self:
        return self.minify()

    def remove_images(self) -> Self:
        self._set_default_output("noimages")
        self._writer.remove_images()
        return self

    def reduce_image_quality(self, quality: Annotated[int, ImageQualityRange]) -> Self:
        self._set_default_output("reduced")
        for page in self._writer.pages:
            for img in page.images:
                img.replace(img.image, quality=quality)
        return self

    def compress(self, compression: Compression = Compression.DEFAULT) -> Self:
        self._set_default_output("compress_{}".format(compression.value))
        for page in self._writer.pages:
            page.compress_content_streams(compression.value)
        return self

    @property
    def info(self) -> Info:
        if self._closed:
            pdf = self.output
        elif self._writer:
            pdf = self._writer
        else:
            pdf = self._reader
        return Info(pdf)

    def watermark(self):
        # todo: add method
        pass
