import os
from tempfile import NamedTemporaryFile
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
from pdfwatermarker.watermark.utils import FONT, resource_path, bundle_dir


def img_opacity(image, opacity, tempdir=None, bw=True):
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
    if bw:
        im.convert('L')
    dst = NamedTemporaryFile(suffix='.png', dir=tempdir, delete=False)
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
