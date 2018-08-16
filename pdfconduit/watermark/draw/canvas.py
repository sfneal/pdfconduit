# Dynamically generate watermark pdf file
import io
from tempfile import NamedTemporaryFile, mkdtemp
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from pdfconduit.utils import resource_path, write_pdf
from pdfconduit.watermark.lib import LETTER
from pdfconduit.watermark.draw.image import img_opacity


class CanvasStr:
    """Canvas string data object used for storing canvas.drawString parameters."""
    def __init__(self, string, font='Vera', color='black', size=40, opacity=0.1, x=0, y=0,
                 x_centered=True, y_centered=False):
        self.string = string
        self.font = font
        self.color = color
        self.size = size
        self.opacity = opacity
        self.x = x
        self.y = y
        self.x_centered = x_centered
        self.y_centered = y_centered


class CanvasImg:
    """Canvas image data object used for storing canvas.drawImage parameters."""
    def __init__(self, image, opacity=0.1, x=0, y=0, w=LETTER[0], h=LETTER[1], mask='auto',
                 preserve_aspect_ratio=True, centered=False):
        self.image = image
        self.opacity = opacity
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.mask = mask
        self.preserve_aspect_ratio = preserve_aspect_ratio
        self.centered = centered


class CanvasObjects:
    """Canvas object collector to store list of canvas objects."""
    def __init__(self):
        self.objects = []

    def __iter__(self):
        return iter(self.objects)

    def add(self, canvas_object):
        self.objects.append(canvas_object)


def center_str(txt, font, size, offset=0):
    text_width = stringWidth(txt, fontName=font, fontSize=size)
    return -(text_width / 2.0) + offset


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
        self.can = Canvas(self.packet, pagesize=LETTER, pageCompression=compress, bottomup=1)  # Initialize canvas

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
        self.can.save()

    def _draw_image(self, canvas_image):
        """Draw Image to canvas"""
        img = img_opacity(canvas_image.image, canvas_image.opacity, tempdir=self.dir)
        self.can.drawImage(img, x=canvas_image.x, y=canvas_image.y, width=canvas_image.w,
                           height=canvas_image.h, mask=canvas_image.mask,
                           preserveAspectRatio=canvas_image.preserve_aspect_ratio, anchorAtXY=True)

    def _draw_string(self, cs):
        """
        Draw string object to reportlabs canvas.

        Canvas Parameter changes (applied if set values differ from string object values
        1. Font name
        2. Font size
        3. Font fill color & opacity
        4. X and Y position

        :param cs: CanvasString Object
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
            x = center_str(cs.string, cs.font, cs.size, offset=0)
            y = ((LETTER[1]) / 2)

        # Y is centered and X is not
        elif cs.y_centered and not cs.x_centered:
            x = cs.x
            y = ((LETTER[1]) / 2)

        # X is centered and Y is not
        elif cs.x_centered and not cs.y_centered:
            x = center_str(cs.string, cs.font, cs.size)
            y = cs.y
        else:
            x = cs.x
            y = cs.y
        self.can.drawString(x=x, y=y, text=cs.string)
