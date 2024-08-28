import os
from abc import ABC
from datetime import datetime
from io import BytesIO
from tempfile import TemporaryDirectory, NamedTemporaryFile
from warnings import warn

from pypdf import PdfWriter, PdfReader

from pdfconduit.internals.exceptions import OutputException
from pdfconduit.utils import pypdf_reader, add_suffix
from pdfconduit.utils.typing import Optional, Any, Dict, Self, PdfObject


class BaseConduit(ABC):
    _path: Optional[str] = None
    _metadata: Dict[str, Any] = {}

    output: Optional[str] = None
    _output_dir: Optional[str] = None
    _closed: bool = False

    _pdf_file = None
    _stream: BytesIO = None
    _reader: PdfReader
    _writer: PdfWriter = None

    _tempdir: Optional[TemporaryDirectory] = None
    _tempfile: Optional[NamedTemporaryFile] = None

    def __init__(
        self, pdf: PdfObject, decrypt_pw: Optional[str] = None, with_writer: bool = True
    ) -> None:
        self._decrypt_pw = decrypt_pw

        if isinstance(pdf, BytesIO):
            self._read_stream(pdf, with_writer)
        else:
            # Open the file & instantiate a PDF reader
            self._path = pdf
            self._open_and_read(with_writer)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            raise exc_val
        self.write()
        return True

    def _open_and_read(self, with_writer: bool = True) -> Self:
        self._pdf_file = open(self._path, "rb")
        self._reader: PdfReader = pypdf_reader(self._pdf_file, self._decrypt_pw)
        if with_writer:
            self._writer: PdfWriter = PdfWriter(clone_from=self._reader)
        return self

    def _read_stream(self, stream: BytesIO, with_writer: bool = True) -> Self:
        self._stream = stream
        self._reader = PdfReader(self._stream, password=self._decrypt_pw)
        if with_writer:
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
        if self._pdf_file is not None:
            self._pdf_file.close()
        if self._stream is not None:
            self._stream.close()

        # Confirm output path is set
        if self.output is None:
            raise OutputException

        # Write the PDF to the output file
        if self._tempdir is not None:
            self._writer.write(self.output)
            self._tempfile.close()
        else:
            with open(self.output, "wb") as output_pdf:
                self._writer.write(output_pdf)

        self._writer.close()

        self._closed = True

        return self.output

    def cleanup(self) -> Self:
        if self._tempdir is not None:
            self._tempdir.cleanup()
        return self

    @property
    def pdf_object(self) -> PdfObject:
        return self._stream if self._stream is not None else self._path

    def write_to_stream(self):
        # todo: implement
        pass

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

    def set_output_temp(
        self, tempdir: Optional[TemporaryDirectory] = None, suffix: str = ""
    ) -> Self:
        self._tempdir = tempdir if tempdir else TemporaryDirectory(prefix="pdfconduit_")
        self._tempfile = NamedTemporaryFile(
            suffix="_" + suffix.replace("_", "") + ".pdf",
            dir=self._tempdir.name,
            delete=False,
        )
        return self.set_output(self._tempfile.name)

    def _set_default_output(self, suffix: str) -> None:
        if self.output is None:
            if self._path is None:
                warn(
                    """
                    Saving PDFs to a temporary directory because an original file directory cannot be determined
                    (likely because we're reading from a stream).  Add a call to `conduit.cleanup() after PDF
                    processing to delete the created temporary directory.
                    """,
                    UserWarning,
                )
                self.set_output_temp(suffix=suffix)
                return
            self.set_output_suffix(suffix)
