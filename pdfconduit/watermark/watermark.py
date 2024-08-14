# Apply a watermark to a PDF file
import os
import shutil
from tempfile import TemporaryDirectory
from typing import Optional

from looptools import Timer

from pdfconduit.pdfconduit import Pdfconduit
from pdfconduit.settings import Encryption
from pdfconduit.utils import add_suffix, Info
from pdfconduit.watermark.add import WatermarkAdd
from pdfconduit.watermark.lib import IMAGE_DEFAULT, IMAGE_DIRECTORY
from pdfconduit.watermark.modify.canvas import CanvasConstructor
from pdfconduit.watermark.modify.draw import WatermarkDraw


class Watermark:
    def __init__(
        self,
        document: str,
        remove_temps: bool = True,
        move_temps: Optional[bool] = None,
        tempdir: Optional[str] = None,
        use_receipt: bool = True,
    ):
        """
        Watermark and encrypt a PDF document.

        Manage watermarking processes from single class initialization.  This class utilizes the draw,
        add and encrypt modules.

        :param document: str
            PDF document full path
        :param remove_temps: bool
            Remove temporary files after completion
        :param open_file: bool
            Open file after completion
        :param tempdir: function or str
            Temporary directory for file writing
        :param receipt: cls
            Use existing Receipt object if already initiated
        :param use_receipt: bool
            Print receipt information to console and write to file
        """
        self.time = Timer()
        self.document_og = document
        self.document = self.document_og
        self.watermark = None
        self.remove_temps = remove_temps
        self.move_temps = move_temps

        if not tempdir:
            self._temp = TemporaryDirectory()
            self.tempdir = self._temp.name
        elif isinstance(tempdir, TemporaryDirectory):
            self._temp = tempdir
            self.tempdir = self._temp.name
        else:
            self.tempdir = tempdir

    def __str__(self) -> str:
        return str(self.document)

    def cleanup(self) -> str:
        runtime = self.time.end
        if self.move_temps:
            if os.path.isdir(self.move_temps):
                shutil.move(self.tempdir, self.move_temps)
        if self.remove_temps:
            if os.path.isdir(self.tempdir):
                shutil.rmtree(self.tempdir)
        return self.document

    def draw(
        self,
        text1: Optional[str] = None,
        text2: Optional[str] = None,
        include_copyright: bool = True,
        image: str = IMAGE_DEFAULT,
        rotate: int = 30,
        opacity: float = 0.08,
        compress: int = 0,
        flatten: bool = False,
        add: bool = False,
    ) -> str:
        """
        Draw watermark PDF file.

        Create watermark using either a reportlabs canvas or a PIL image.

        :param text1: str
            Text line 1
        :param text2: str
            Text line 2
        :param include_copyright: bool
            Draw copyright and year to canvas
        :param image: str
            Logo image to be used as base watermark
        :param rotate: int
            Degrees to rotate canvas by
        :param opacity: float
            Watermark opacity
        :param compress: bool
            Compress watermark contents  (not entire PDF)
        :param flatten: bool
            Draw watermark with multiple layers or a single flattened layer
        :param add: bool
            Add watermark to original document
        :return: str
            Watermark PDF file full path
        """
        im_path = os.path.join(IMAGE_DIRECTORY, image)
        if os.path.isfile(im_path):
            image = im_path

        co = CanvasConstructor(
            text1,
            text2,
            include_copyright,
            image,
            rotate,
            opacity,
            tempdir=self.tempdir,
        )
        objects, rotate = (
            co.img() if flatten else co.canvas()
        )  # Run img constructor method if flatten is True

        # Draw watermark to file
        self.watermark = WatermarkDraw(
            objects,
            rotate=rotate,
            compress=compress,
            tempdir=self.tempdir,
            pagesize=Info(self.document_og).size,
            pagescale=True,
        ).write()

        if not add:
            return self.watermark
        else:
            self.add()
            return self.cleanup()

    def add(
        self,
        document: Optional[str] = None,
        watermark: Optional[str] = None,
        underneath: bool = False,
        output: Optional[str] = None,
        suffix: Optional[str] = "watermarked",
        method: str = "pdfrw",
    ) -> str:
        """
        Add a watermark file to an existing PDF document.

        Rotate and upscale watermark file as needed to fit existing PDF document.  Watermark can be overlayed or
        placed underneath.

        :param document: str
            PDF document full path
        :param watermark: str
            Watermark PDF full path
        :param underneath: bool
            Place watermark either under or over existing PDF document
        :param output: str
            Output file path
        :param suffix: str
            Suffix to append to existing PDF document file name
        :param method: str
            PDF library to be used for watermark adding
        :return: str
            Watermarked PDF Document full path
        """
        if not watermark:
            watermark = self.watermark
        if not document:
            document = self.document

        watermarker = WatermarkAdd(
            document,
            watermark,
            output=output,
            underneath=underneath,
            tempdir=self.tempdir,
            suffix=suffix,
        )
        if method == "pdfrw":
            watermarker.use_pdfrw()
        else:
            watermarker.use_pypdf()
        self.document = watermarker.add()

        return self.document

    def encrypt(
        self,
        user_pw: str = "",
        owner_pw: Optional[str] = None,
        encrypt_128: bool = True,
        allow_printing: bool = True,
        allow_commenting: bool = False,
        document: Optional[str] = None,
    ):
        """
        Encrypt a PDF document to add passwords and restrict permissions.

        Add a user password that must be entered to view document and a owner password that must be entered to alter
        permissions and security settings.  Encryption keys are 128 bit when encrypt_128 is True and 40 bit when
        False.  By default permissions are restricted to print only, when set to false all permissions are allowed.
        TODO: Add additional permission parameters

            User password required to open and view PDF document
        :param owner_pw: str
            Owner password required to alter security settings and permissions
        :param encrypt_128: bool
            Encrypt PDF document using 128 bit keys
        :param allow_printing: bool
            Restrict permissions to print only
        :param allow_commenting:
        :param user_pw: str
        :param document:
        :return: str
            Encrypted PDF full path
        """
        document = self.document if document is None else document

        encrypter = Encryption(
            user_pw=user_pw,
            owner_pw=owner_pw,
            allow_printing=allow_printing,
            allow_commenting=allow_commenting,
        )
        p = (
            Pdfconduit(document)
            .set_output(add_suffix(self.document_og, "secured"))
            .encrypt(encrypter)
            .write()
        )

        return p
