# Dynamically generate watermark pdf file
import io
import os
from tempfile import NamedTemporaryFile, mkdtemp
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from pdfwatermarker.utils import resource_path, write_pdf
from pdfwatermarker.watermark.lib import image_directory, LETTER
from pdfwatermarker.watermark.draw._objects import CanvasImg, CanvasStr
from pdfwatermarker.watermark.draw.image import img_opacity


def available_images():
    return sorted([i for i in os.listdir(image_directory) if not i.startswith('.')], reverse=True)


def center_str(txt, font, size, offset=120):
    page_width = LETTER[0]
    text_width = stringWidth(txt, fontName=font, fontSize=size)
    return ((page_width - text_width) / 2.0) + offset


class Draw:
    def __init__(self, tempdir=None, compress=0):
        if tempdir:
            self.dir = tempdir
        else:
            self.dir = mkdtemp()
        tmppdf = NamedTemporaryFile(suffix='.pdf', dir=self.dir, delete=False)
        self.dst = resource_path(tmppdf.name)

        # create a new PDF with Reportlab
        self.packet = io.BytesIO()
        self.can = Canvas(self.packet, pagesize=LETTER, pageCompression=compress)  # Initialize canvas

    def __str__(self):
        return str(self.dst)

    def _write(self):
        self.packet.seek(0)  # move to the beginning of the StringIO buffer
        write_pdf(self.packet, self.dst)  # Save new pdf file
        return self.dst

    def write(self):
        return self._write()


class WatermarkDraw(Draw):
    def __init__(self, canvas_objects, rotate=0, compress=0, tempdir=None):
        super(WatermarkDraw, self).__init__(tempdir, compress)
        self.canvas_objects = canvas_objects
        self.rotate = rotate

        self.draw()

    def draw(self):
        # Rotate canvas
        self.can.rotate(self.rotate)

        # Iterate canvas objects and determine if string or image
        for obj in self.canvas_objects:
            if isinstance(obj, CanvasStr):
                self._draw_string(obj)
            elif isinstance(obj, CanvasImg):
                self._draw_image(obj)
        self.can.save()

    def _draw_image(self, canvas_image):
        """Draw Image to canvas"""
        img = img_opacity(canvas_image.image, canvas_image.opacity, tempdir=self.dir)
        self.can.drawImage(img.name, x=canvas_image.x, y=canvas_image.y, width=canvas_image.w,
                           height=canvas_image.h, mask=canvas_image.mask,
                           preserveAspectRatio=canvas_image.preserve_aspect_ratio)

    def _draw_string(self, canvas_string):
        """Draw string to canvas"""
        # Set font names and font sizes if different from current object params
        if self.can._fontname != canvas_string.font:
            self.can.setFont(canvas_string.font, canvas_string.size)
        elif self.can._fontsize != canvas_string.size:
            self.can.setFontSize(canvas_string.size)
        assert self.can._fontname == canvas_string.font
        assert self.can._fontsize == canvas_string.size

        self.can.setFillColor(canvas_string.color, canvas_string.opacity)

        if canvas_string.y_centered and canvas_string.x_centered:
            x = center_str(canvas_string.string, canvas_string.font, canvas_string.size, offset=0)
            y = ((LETTER[1]) / 2)
        elif canvas_string.y_centered and not canvas_string.x_centered:
            x = canvas_string.x
            y = ((LETTER[1]) / 2)
        elif canvas_string.x_centered and not canvas_string.y_centered:
            x = center_str(canvas_string.string, canvas_string.font, canvas_string.size)
            y = canvas_string.y
        else:
            x = canvas_string.x
            y = canvas_string.y

        self.can.drawString(x=x, y=y, text=canvas_string.string)
