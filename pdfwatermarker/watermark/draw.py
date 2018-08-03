# Dynamically generate watermark pdf file
import io
import os
import sys
from tempfile import NamedTemporaryFile, mkdtemp
from PIL import Image, ImageEnhance
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pdfwatermarker import resource_path, write_pdf


def bundle_dir():
    """Handle resource management within an executable file."""
    if getattr(sys, 'frozen', False):
        # we are running in a bundle
        bundle_dir = sys._MEIPASS
    else:
        # we are running in a normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
    return bundle_dir


def register_font():
    """Register fonts for report labs canvas."""
    folder = bundle_dir + os.sep + 'lib'
    ttfFile = resource_path(os.path.join(folder, 'Vera.ttf'))
    pdfmetrics.registerFont(TTFont("Vera", ttfFile))


bundle_dir = bundle_dir()
register_font()
LETTER = letter[1], letter[0]
image_directory = str(bundle_dir + os.sep + 'lib' + os.sep + 'img')


def available_images():
    imgs = sorted([i for i in os.listdir(image_directory) if not i.startswith('.')],
                  reverse=True)
    return imgs


def center_str(txt, font, size, offset=120):
    page_width = letter[1]
    text_width = stringWidth(txt, fontName=font, fontSize=size)
    return ((page_width - text_width) / 2.0) + offset


def img_opacity(image, opacity, tempdir=None):
    """
    Returns an image with reduced opacity.
    Taken from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/362879
    """
    dst = NamedTemporaryFile(suffix='.png', dir=tempdir, delete=False)
    assert 0 <= opacity <= 1
    im = Image.open(image)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    im.save(dst)
    return dst


class CanvasStr:
    """Canvas string data object used for storing canvas.drawString parameters."""
    def __init__(self, string, font='Vera', color='black', size=40, opacity=0.1, x=None, y=None,
                 x_centered=True):
        self.string = string
        self.font = font
        self.color = color
        self.size = size
        self.opacity = opacity
        self.x = x
        self.y = y
        self.x_centered = x_centered


class CanvasImg:
    """Canvas image data object used for storing canvas.drawImage parameters."""
    def __init__(self, image, opacity=0.1, x=0, y=0, w=letter[0], h=letter[1], mask='auto',
                 preserve_aspect_ratio=True):
        self.image = image
        self.opacity = opacity
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.mask = mask
        self.preserve_aspect_ratio = preserve_aspect_ratio


class CanvasObjects:
    """Canvas object collector to store list of canvas objects."""
    def __init__(self):
        self.objects = []

    def __iter__(self):
        return iter(self.objects)

    def add(self, canvas_object):
        self.objects.append(canvas_object)


class Draw:
    def __init__(self, tempdir=None, compress=0):
        if tempdir:
            self.dir = tempdir
        else:
            self.dir = mkdtemp()
        tmppdf = NamedTemporaryFile(suffix='.pdf', dir=tempdir, delete=False)
        self.dst = resource_path(tmppdf.name)

        # create a new PDF with Reportlab
        self.packet = io.BytesIO()
        self.can = Canvas(self.packet, pagesize=LETTER, pageCompression=compress)  # Initialize canvas

    def __str__(self):
        return str(self.dst)

    def write(self):
        self.packet.seek(0)  # move to the beginning of the StringIO buffer
        write_pdf(self.packet, self.dst)  # Save new pdf file
        return self.dst


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

        # Save canvas
        # self.can.showPage()
        self.can.save()

    def _draw_image(self, canvas_image):
        """Draw Image to canvas"""
        img = img_opacity(canvas_image.image, canvas_image.opacity, self.dir)
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

        if canvas_string.x_centered:
            x = center_str(canvas_string.string, canvas_string.font, canvas_string.size)
        else:
            x = canvas_string.x
        self.can.drawString(x=x, y=canvas_string.y, text=canvas_string.string)
