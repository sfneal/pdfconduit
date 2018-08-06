import os
from tempfile import NamedTemporaryFile
from reportlab.lib.pagesizes import letter
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
from pdfwatermarker.watermark.utils import FONT, resource_path, bundle_dir


class CanvasStr:
    """Canvas string data object used for storing canvas.drawString parameters."""
    def __init__(self, string, font='Vera', color='black', size=40, opacity=0.1, x=None, y=None,
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


def img_opacity(image, opacity, tempdir=None, bw=True):
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
    if bw:
        im.convert('L')
    im.save(dst)
    return dst


class DrawPIL:
    def __init__(self, size=(792, 612)):
        # Create a black image
        self.img = Image.new('RGBA', size, color=(255, 255, 255, 0))  # 2200, 1700 for 200 DPI

    def _centered_text(self, text, drawing, font):
        # Get img size
        page_width = self.img.size
        text_width = drawing.textsize(text, font=font)
        x = (page_width[0] - text_width[0]) / 2
        return x

    def draw_text(self, text, x='center', y=140, font=FONT, size=40, opacity=0.1):
        # Set drawing context
        d = ImageDraw.Draw(self.img)

        # Set a font
        fnt = ImageFont.truetype(font, int(size * 1.25))

        # Check if x is set to 'center'
        if 'center' in str(x).lower():
            x = self._centered_text(text, d, fnt)

        # Draw text to image
        d.text((x, y), text, font=fnt, fill=(0, 0, 0, int(255 / (opacity * 100))))

    def save(self, destination=None, file_name='pil', tempdir=None):
        fn = file_name.strip('.png') if '.png' in file_name else file_name
        if tempdir:
            tmpimg = NamedTemporaryFile(suffix='.png', dir=tempdir, delete=False)
            output = resource_path(tmpimg.name)
        elif destination:
            output = os.path.join(destination, fn + '.png')
        else:
            output = os.path.join(bundle_dir(), fn + '.png')

        # Save image file
        self.img.save(output)
        return output
