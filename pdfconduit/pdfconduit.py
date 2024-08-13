import os
from datetime import datetime

from pypdf import PdfWriter, PdfReader

from pdfconduit import Merge
from pdfconduit.compression import Compression, ImageQualityRange
from pdfconduit.convert import Flatten
from pdfconduit.encryption import Encryption
from pdfconduit.transform import Rotate, Upscale
from pdfconduit.utils import Info, pypdf_reader, add_suffix
from pdfconduit.utils.typing import Optional, Any, Tuple, Dict, Self, Annotated


class Conduit:
    _metadata: Dict[str, Any] = {}

    output: Optional[str] = None
    _output_dir: Optional[str] = None
    _closed: bool = False

    _pdf_file = None
    _reader: PdfReader
    _writer: PdfWriter

    def __init__(self, path: str, decrypt_pw: Optional[str] = None) -> None:
        self._path = path
        self._decrypt_pw = decrypt_pw

        # Open the file & instantiate a PDF reader
        self._open_and_read()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            raise exc_val
        self.write()
        return True

    def _open_and_read(self) -> Self:
        self._pdf_file = open(self._path, "rb")
        self._reader: PdfReader = pypdf_reader(self._pdf_file, self._decrypt_pw)
        self._writer: PdfWriter = PdfWriter(clone_from=self._reader)
        return self

    def write(self):
        # Set default output in case none was set
        self._set_default_output("modified")

        # Add metadata
        # Format the current date and time for the metadata
        utc_time = "-05'00'"  # UTC time optional
        time = datetime.now().strftime(f"D\072%Y%m%d%H%M%S{utc_time}")
        default_metadata = {
            "/Producer": "pdfconduit",
            "/Creator": "pdfconduit",
            "/Author": "pdfconduit",
            "/ModDate": time,
        }
        default_metadata.update(self._metadata)
        self._writer.add_metadata(default_metadata)

        # Close the PDF reader & file reader
        self._reader.close()
        self._pdf_file.close()

        # Write the PDF to the output file
        with open(self.output, "wb") as output_pdf:
            self._writer.write(output_pdf)

        self._writer.close()
        self._pdf_file.close()

        self._closed = True

        return self.output

    def set_metadata(self, metadata: Dict[str, Any]) -> Self:
        self._metadata = metadata
        return self

    def set_output(self, output: str) -> Self:
        self.output = output
        return self

    def set_output_suffix(self, suffix: str) -> Self:
        return self.set_output(
            add_suffix(
                (
                    os.path.join(self._output_dir, os.path.basename(self._path))
                    if self._output_dir is not None
                    else self._path
                ),
                suffix,
            )
        )

    def set_output_directory(self, directory: str) -> Self:
        self._output_dir = directory
        return self

    def _set_default_output(self, suffix: str) -> None:
        if self.output is None:
            self.set_output_suffix(suffix)

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
        self._set_default_output("merged")
        if position is None:
            self._writer.append(pdf)
        else:
            self._writer.merge(position, pdf)
        return self

    def merge_fast(self, pdfs: list) -> Self:
        self._set_default_output("merged")
        self._path = (
            Merge([self._path] + pdfs, output_dir=self._output_dir).use_pdfrw().merge()
        )
        return self._open_and_read()

    def rotate(self, degrees: int) -> Self:
        self._set_default_output("rotated")
        for page in self._writer.pages:
            page.rotate(degrees)
        return self

    def rotate_exact(self, degrees: int) -> Self:
        if degrees % 90 == 0:
            return self.rotate(degrees)

        self._path = Rotate(self._path, degrees).use_pdfrw().rotate()
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
                Upscale(
                    self._path,
                    margin_x=x,
                    margin_y=y,
                    scale=scale,
                    tempdir=self._output_dir,
                )
                .use_pdfrw()
                .upscale()
            )
            return self._open_and_read()

        width, height = self.info.size
        width, height = (width * scale, height * scale)
        for page in self._writer.pages:
            page.scale_to(width, height)
        return self

    def flatten(self) -> Self:
        # todo: re-write Flatten & other convert classes
        self._path = Flatten(
            self._path, suffix="flattened", tempdir=self._output_dir
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
        return Info(self._writer if not self._closed else self.output)

    def watermark(self):
        # todo: add method
        pass
