import os
from abc import ABC
from datetime import datetime

from pypdf import PdfWriter, PdfReader

from pdfconduit.utils import pypdf_reader, add_suffix
from pdfconduit.utils.typing import Optional, Any, Dict, Self


class BaseConduit(ABC):
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