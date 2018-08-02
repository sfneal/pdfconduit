# Dynamically generate watermark pdf file
import io
import os
import sys
import shutil
from PIL import Image, ImageEnhance
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pdfwatermarker import set_destination, resource_path, overlay_pdfs, write_pdf
from pdfwatermarker.watermark.add import WatermarkAdd


def remove_temp(pdf):
    temp = os.path.join(os.path.dirname(pdf), 'temp')
    shutil.rmtree(temp)


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
default_template = resource_path(bundle_dir + os.sep + 'lib' + os.sep + 'watermark.pdf')
default_image = resource_path(bundle_dir + os.sep + 'lib' + os.sep + 'watermark.png')
LETTER = letter[1], letter[0]


def center_str(txt, font, size, offset=120):
    page_width = letter[1]
    text_width = stringWidth(txt, fontName=font, fontSize=size)
    return ((page_width - text_width) / 2.0) + offset


def img_opacity(image, opacity):
    """
    Returns an image with reduced opacity.
    Taken from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/362879
    """
    assert 0 <= opacity <= 1
    im = Image.open(image)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im


class CanvasStr:
    def __init__(self, string, font='Vera', color='black', size=40, opacity=0.1, rotate=0, x=None, y=None,
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
    def __init__(self):
        self.objects = []

    def __str__(self):
        return str(self.objects)

    def __iter__(self):
        return iter(self.objects)

    def add(self, canvas_object):
        self.objects.append(canvas_object)

    def get(self):
        return self.objects


class Draw:
    def __init__(self, dst):
        self.dst = dst

        # create a new PDF with Reportlab
        self.packet = io.BytesIO()
        self.can = Canvas(self.packet, pagesize=LETTER)  # Initialize canvas

    def __str__(self):
        return str(self.dst)

    def write(self):
        self.packet.seek(0)  # move to the beginning of the StringIO buffer
        write_pdf(self.packet, self.dst)  # Save new pdf file


class TextDraw(Draw):
    def __init__(self, file_name, text, font='Vera', opacity=1, font_size=16, font_color='black',
                 output_overwrite=False):
        dst = resource_path(set_destination(file_name, 'text'))
        super(TextDraw, self).__init__(dst, font, opacity, font_size, font_color)

        self.text = text
        self.draw()
        self.write()
        w = WatermarkAdd(file_name, self.dst, overwrite=output_overwrite, suffix='text')
        remove_temp(file_name)

    def draw(self):
        """Draw text to canvas"""
        # Address
        self.can.setFont(self.font, self.font_size)  # Large font for address
        self.can.setFillColor(self.font_color, self.opacity)
        self.can.drawString(x=30, y=20, text=self.text)
        self.can.save()  # Save canvas


class WatermarkDraw(Draw):
    def __init__(self, project, pdf, canvas_objects, rotate=0):
        dst = resource_path(set_destination(pdf, project, 'watermark'))
        super(WatermarkDraw, self).__init__(dst)

        self.canvas_objects = canvas_objects

        self.rotate = rotate
        self.img_dst = resource_path(set_destination(pdf, project, 'watermark_img', '.png'))
        self.draw()
        self.write()

    def draw(self):
        # Draw watermark elements
        self.can.rotate(self.rotate)
        for obj in self.canvas_objects:
            if isinstance(obj, CanvasStr):
                self._draw_string(obj)
            elif isinstance(obj, CanvasImg):
                self._draw_image(obj)
        self.can.save()  # Save canvas

    def _draw_image(self, canvas_image):
        """Draw HPA Logo to canvas (Layer 1)"""
        if canvas_image:
            img = img_opacity(canvas_image.image, canvas_image.opacity)
            img.save(self.img_dst)
            self.can.drawImage(self.img_dst, x=canvas_image.x, y=canvas_image.y, width=canvas_image.w,
                               height=canvas_image.h, mask=canvas_image.mask,
                               preserveAspectRatio=canvas_image.preserve_aspect_ratio)

    def _draw_string(self, canvas_string):
        if canvas_string:
            self.can.setFont(canvas_string.font, canvas_string.size)
            self.can.setFillColor(canvas_string.color, canvas_string.opacity)
            if canvas_string.x_centered:
                x = center_str(canvas_string.string, canvas_string.font, canvas_string.size)
            else:
                x = canvas_string.x
            self.can.drawString(x=x, y=canvas_string.y, text=canvas_string.string)
