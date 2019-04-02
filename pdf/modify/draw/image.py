import os
from tempfile import NamedTemporaryFile
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
from PyBundle import bundle_dir, resource_path
from pdf.modify import FONT


def img_opacity(image, opacity, tempdir=None, bw=True):
    """
    Reduce the opacity of a PNG image.

    Inspiration: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/362879

    :param image: PNG image file
    :param opacity: float representing opacity percentage
    :param tempdir: Temporary directory
    :param bw: Set image to black and white
    :return:  Path to modified PNG
    """
    # Validate parameters
    try:
        assert 0 <= opacity < 1
    except AssertionError:
        return image
    assert os.path.isfile(image), 'Image is not a file'

    # Open image in RGBA mode if not already in RGBA
    with Image.open(image) as im:
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        else:
            im = im.copy()

        # Adjust opacity
        alpha = im.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        im.putalpha(alpha)
        if bw:
            im.convert('L')

        # Save modified image file
        with NamedTemporaryFile(suffix='.png', dir=tempdir, delete=False) as dst:
            im.save(dst)
            return dst.name


class DrawPIL:
    def __init__(self, size=(792, 612), tempdir=None):
        # Create a black image
        self.img = Image.new('RGBA', size, color=(255, 255, 255, 0))  # 2200, 1700 for 200 DPI
        self.tempdir = tempdir

    def _centered_x(self, text, drawing, font_type):
        """
        Retrieve a 'x' value that centers the image in the canvas.

        :param text: String to be centered
        :param drawing: PIL.ImageDraw.Draw instance
        :param font_type: Registered font family type
        :return: X coordinate value
        """
        # ('Page Width' - 'Text Width') / 2
        return (self.img.size[0] - drawing.textsize(text, font=font_type)[0]) / 2

    def _centered_y(self, font_size):
        """
        Retrieve a 'y' value that centers the image in the canvas.

        :param font_size: Font size
        :return: Y coordinate value
        """
        # ('Image Size' / 2) - 'Font Size'
        return (self.img.size[1] / 2) - font_size

    def _scale(self, img, func='min'):
        im = img if isinstance(img, Image.Image) else Image.open(img)

        if func is 'min':
            scale = min(float(self.img.size[0] / im.size[0]), float(self.img.size[1] / im.size[1]))
        else:
            scale = max(float(self.img.size[0] / im.size[0]), float(self.img.size[1] / im.size[1]))

        im.thumbnail((int(im.size[0] * scale), int(im.size[1] * scale)))

        image = im if isinstance(img, Image.Image) else self.save(img=im)
        im.close()
        return image

    def draw_text(self, text, x='center', y=140, font=FONT, size=40, opacity=25):
        # Set drawing context
        d = ImageDraw.Draw(self.img)

        # Set a font
        fnt = ImageFont.truetype(font, int(size * 1.00))  # multiply size of font if needed

        # Check if x or y is set to 'center'
        x = self._centered_x(text, d, fnt) if 'center' in str(x).lower() else x
        y = self._centered_y(size) if 'center' in str(y).lower() else y

        # Draw text to image
        d.text((x, y), text, font=fnt, fill=(0, 0, 0, opacity))

    def draw_img(self, img, x=0, y=0, opacity=1.0):
        scaled = self._scale(img)
        opacity = Image.open(img_opacity(scaled, opacity, self.tempdir))
        self.img.paste(opacity, (x, y))

    def rotate(self, rotate):
        # Create transparent image that is the same size as self.img
        mask = Image.new('L', self.img.size, 255)

        # Rotate image and then scale image to fit self.img
        front = self.img.rotate(rotate, expand=True)

        # Rotate mask
        mask.rotate(rotate, expand=True)

        # Determine difference in size between mask and front
        y_margin = int((mask.size[1] - front.size[1]) / 3)

        # Create another new image
        rotated = Image.new('RGBA', self.img.size, color=(255, 255, 255, 0))

        # Paste front into new image and set x offset equal to half
        # the difference of front and mask size
        rotated.paste(front, (0, y_margin))
        self.img = rotated

    def save(self, img=None, destination=None, file_name='pil'):
        img = self.img if not img else img
        fn = file_name.strip('.png') if '.png' in file_name else file_name
        if self.tempdir:
            tmpimg = NamedTemporaryFile(suffix='.png', dir=self.tempdir, delete=False)
            output = resource_path(tmpimg.name)
            tmpimg.close()
        elif destination:
            output = os.path.join(destination, fn + '.png')
        else:
            output = os.path.join(bundle_dir(), fn + '.png')

        # Save image file
        img.save(output)
        return output
