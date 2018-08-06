import os
from tempfile import NamedTemporaryFile
from reportlab.lib.pagesizes import letter
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
from pdfwatermarker.watermark.utils import FONT


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


def center_text(text, page_width, drawing, font):
    text_width = drawing.textsize(text, font=font)
    s = (page_width[0] - text_width[0]) / 2
    print(s)
    return s


def pil_save(img, destination, file_name='letter'):
    # Save image file
    output = os.path.join(destination, file_name.strip('.png') + '.png')
    img.save(output)
    return output


def pil_create_letter(size=(792, 612)):
    # Create a black image
    img = Image.new('RGBA', size, color=(255, 255, 255, 0))  # 2200, 1700 for 200 DPI
    return img


def pil_draw_text_centered(img, text, y=140, font=FONT, size=40, opacity=0.1):
    # Get img size
    img_size = img.size

    # Set drawing context
    d = ImageDraw.Draw(img)

    # Set a font
    fnt = ImageFont.truetype(font, size)

    # Draw text to image
    s = center_text(text, img_size, d, fnt)
    d.text((s, y), text, font=fnt, fill=(0, 0, 0, int(255 / (opacity * 100))))
    return img

