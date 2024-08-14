# Dynamically generate watermark pdf file
import io
from tempfile import NamedTemporaryFile, mkdtemp
from typing import Tuple, Optional

from PillowImage import img_adjust
from PyBundle import resource_path
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas

from pdfconduit.utils.write import write_pdf
from pdfconduit.watermark.modify import LETTER
from pdfconduit.watermark.modify.canvas import CanvasStr, CanvasImg, CanvasObjects


def text_width(string: str, font_name: str = "Vera", font_size: int = 40) -> float:
    """Determine with width in pixels of string."""
    return stringWidth(string, fontName=font_name, fontSize=font_size)


def center_str(txt: str, font_name: str, font_size: int, offset: int = 0) -> float:
    """Center a string on the x-axis of a reportslab canvas"""
    return -(text_width(txt, font_name, font_size) / 2.0) + offset


def split_str(string: str) -> Tuple[str, str]:
    """Split string in half to return two strings"""
    split = string.split(" ")
    return " ".join(split[: len(split) // 2]), " ".join(split[len(split) // 2 :])


class DrawPDF:
    def __init__(
        self,
        tempdir: Optional[str] = None,
        compress: int = 0,
        pagesize: Tuple[float, float] = LETTER,
    ):
        if tempdir:
            self.dir = tempdir
        else:
            self.dir = mkdtemp()

        self._dst = None

        # create a new PDF with Reportlab
        self.packet = io.BytesIO()
        self.can = Canvas(
            self.packet, pagesize=pagesize, pageCompression=compress, bottomup=1
        )  # Initialize canvas

    def __str__(self) -> str:
        return str(self.dst)

    @property
    def dst(self) -> str:
        if not self._dst:
            with NamedTemporaryFile(
                suffix=".pdf", dir=self.dir, delete=False
            ) as tmppdf:
                self._dst = resource_path(tmppdf.name)
        return self._dst

    def _write(self, output: Optional[str] = None) -> str:
        self.packet.seek(0)  # move to the beginning of the StringIO buffer
        output = output if output else self.dst
        write_pdf(self.packet, output)  # Save new pdf file
        return output

    def write(self, output: Optional[str] = None) -> str:
        return self._write(output)


class WatermarkDraw(DrawPDF):
    def __init__(
        self,
        canvas_objects: CanvasObjects,
        rotate: int = 0,
        compress: int = 0,
        pagesize: Tuple[float, float] = LETTER,
        tempdir: Optional[str] = None,
        pagescale: bool = False,
    ):
        super(WatermarkDraw, self).__init__(tempdir, compress, pagesize)
        self.canvas_objects = canvas_objects
        self.rotate = rotate

        # Scale width, height and font size if pagesize is not letter sized
        if pagescale and self.can._pagesize != LETTER:
            w_scale = self.can._pagesize[0] / LETTER[0]
            h_scale = self.can._pagesize[1] / LETTER[1]
            for i in self.canvas_objects:
                if hasattr(i, "w"):
                    i.w = i.w * w_scale
                if hasattr(i, "h"):
                    i.h = i.h * h_scale
                if hasattr(i, "size"):
                    i.size = i.size * ((h_scale * w_scale) / 2)

        self.draw()

    def draw(self) -> None:
        # Move canvas origin to the middle of the page
        self.can.translate(self.can._pagesize[0] / 2, self.can._pagesize[1] / 2)

        # Rotate canvas
        self.can.rotate(self.rotate)

        # Iterate canvas objects and determine if string or image
        for obj in self.canvas_objects:
            # Adjust x and y based on rotation
            obj.x += int(self.rotate * 1.5)
            obj.y += -int(self.rotate * 3)

            # Check if CanvasObject is a string or image
            if isinstance(obj, CanvasStr):
                self._draw_string(obj)
            elif isinstance(obj, CanvasImg):
                self._draw_image(obj)
        self.can.showPage()
        self.can.save()

    def _draw_image(self, ci: CanvasImg) -> None:
        """
        Draw image object to reportlabs canvas.

        :param ci: CanvasImage object
        """
        img = img_adjust(ci.image, ci.opacity, tempdir=self.dir)
        self.can.drawImage(
            img,
            x=ci.x,
            y=ci.y,
            width=ci.w,
            height=ci.h,
            mask=ci.mask,
            preserveAspectRatio=ci.preserve_aspect_ratio,
            anchorAtXY=True,
        )

    def _draw_string(self, cs: CanvasStr) -> None:
        """
        Draw string object to reportlabs canvas.

        Canvas Parameter changes (applied if set values differ from string object values)
        1. Font name
        2. Font size
        3. Font fill color & opacity
        4. X and Y position

        :param cs: CanvasString object
        """
        # 1. Font name
        if self.can._fontname != cs.font:
            self.can.setFont(cs.font, cs.size)

        # 2. Font size
        elif self.can._fontsize != cs.size:
            self.can.setFontSize(cs.size)

        # 3. Font file color
        self.can.setFillColor(cs.color, cs.opacity)

        # 4. X and Y positions
        # X and Y are both centered
        if cs.y_centered and cs.x_centered:
            # Check if text_width is greater than the canvas page width
            if text_width(cs.string, cs.font, cs.size) > self.can._pagesize[0]:
                str1, str2 = split_str(cs.string)
                self.can.drawString(
                    x=center_str(str1, cs.font, cs.size, offset=0), y=cs.size, text=str1
                )
                self.can.drawString(
                    x=center_str(str2, cs.font, cs.size, offset=0),
                    y=-cs.size,
                    text=str2,
                )
                return
            else:
                x = center_str(cs.string, cs.font, cs.size, offset=0)
                y = 0

        # Y is centered and X is not
        elif cs.y_centered and not cs.x_centered:
            x = cs.x
            y = 0

        # X is centered and Y is not
        elif cs.x_centered and not cs.y_centered:
            x = center_str(cs.string, cs.font, cs.size, offset=0)
            y = cs.y
        else:
            x = cs.x
            y = cs.y
        self.can.drawString(x=x, y=y, text=cs.string)
        return
