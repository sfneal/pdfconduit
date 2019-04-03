import os
from tempfile import NamedTemporaryFile
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
from PyBundle import bundle_dir, resource_path
from pdf.modify import FONT


def img_adjust(image, opacity=1.0, rotate=None, fit=0, tempdir=None, bw=False):
    """
    Reduce the opacity of a PNG image or add rotation.

    Inspiration: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/362879

    :param image: PNG image file
    :param opacity: float representing opacity percentage
    :param rotate: Degrees to rotate
    :param fit: If true, expands the size of the image to fit the whole canvas
    :param tempdir: Temporary directory
    :param bw: Set image to black and white
    :return:  Path to modified PNG
    """
    # Validate parameters
    if opacity:
        try:
            assert 0 <= opacity <= 1
        except AssertionError:
            return image
    assert os.path.isfile(image), 'Image is not a file'

    # Open image in RGBA mode if not already in RGBA
    with Image.open(image) as im:
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        else:
            im = im.copy()

        if rotate:
            # Rotate the image
            if rotate == 90:
                im = im.transpose(Image.ROTATE_90)
            elif rotate == 180:
                im = im.transpose(Image.ROTATE_180)
            elif rotate == 270:
                im = im.transpose(Image.ROTATE_270)
            else:
                im = im.rotate(rotate, expand=fit)

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
    def __init__(self, img=None, size=(792, 612), tempdir=None):
        # Create a black image
        if img:
            self.img = Image.open(img)
            self.img = self.img.convert('RGBA') if self.img.mode != 'RGBA' else self.img.copy()
        else:
            self.img = Image.new('RGBA', size, color=(255, 255, 255, 0))  # 2200, 1700 for 200 DPI
        self.tempdir = tempdir

    @property
    def size(self):
        """Return a tuple (Width, Height) with image dimensions."""
        return self.img.size

    @property
    def width(self):
        """Return the width value of the image's dimensions."""
        return self.size[0]

    @property
    def height(self):
        """Return the height value of the image's dimensions."""
        return self.size[1]

    def _text_centered_x(self, text, drawing, font_type):
        """
        Retrieve a 'x' value that centers the image in the canvas.

        :param text: String to be centered
        :param drawing: PIL.ImageDraw.Draw instance
        :param font_type: Registered font family type
        :return: X coordinate value
        """
        # ('Page Width' - 'Text Width') / 2
        return (self.width - drawing.textsize(text, font=font_type)[0]) / 2

    def _text_centered_y(self, font_size):
        """
        Retrieve a 'y' value that centers the image in the canvas.

        :param font_size: Font size
        :return: Y coordinate value
        """
        # ('Image Size' / 2) - 'Font Size'
        return (self.height / 2) - font_size

    def scale(self, img, func='min'):
        """Scale an image to fit the Pillow canvas."""
        im = img if isinstance(img, Image.Image) else Image.open(img)

        # Use either the shortest edge (min) or the longest edge (max) to determine scale factor
        if func is 'min':
            scale = min(float(self.width / im.size[0]), float(self.height / im.size[1]))
        else:
            scale = max(float(self.width / im.size[0]), float(self.height / im.size[1]))

        im.thumbnail((int(im.size[0] * scale), int(im.size[1] * scale)))

        image = im if isinstance(img, Image.Image) else self.save(img=im)
        im.close()
        return image

    def draw_text(self, text, x='center', y=140, font=FONT, font_size=40, opacity=25):
        """
        Draw text onto a Pillow image canvas.
        
        :param text: Text string 
        :param x: X coordinate value
        :param y: Y coordinate value
        :param font: Registered font family 
        :param font_size: Font size
        :param opacity: Opacity of text to be drawn
        :return: 
        """
        # Set drawing context
        d = ImageDraw.Draw(self.img)

        # Set a font
        fnt = ImageFont.truetype(font, int(font_size * 1.00))  # multiply size of font if needed

        # Check if x or y is set to 'center'
        x = self._text_centered_x(text, d, fnt) if 'center' in str(x).lower() else x
        y = self._text_centered_y(font_size) if 'center' in str(y).lower() else y

        # Draw text to image
        opacity = int(opacity * 100) if opacity < 1 else opacity
        d.text((x, y), text, font=fnt, fill=(0, 0, 0, opacity))

    def draw_img(self, img, x=0, y=0, opacity=1.0, rotate=0, fit=1):
        """
        Scale an image to fit the canvas then alpha composite paste the image.

        Optionally place the image (x, y), adjust the images opacity
        or apply a rotation.

        :param img: Path to image to paste
        :param x: X coordinates value (Left)
        :param y: Y coordinates value (Top)
        :param opacity: Opacity value
        :param rotate: Rotation degrees
        :param fit: When true, expands image canvas size to fit rotated image
        :return:
        """
        self.img.alpha_composite(Image.open(img_adjust(self.scale(img), opacity, rotate, fit, self.tempdir)), (x, y))

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
        if destination:
            output = os.path.join(destination, fn + '.png')
        elif self.tempdir:
            tmpimg = NamedTemporaryFile(suffix='.png', dir=self.tempdir, delete=False)
            output = resource_path(tmpimg.name)
            tmpimg.close()
        else:
            output = os.path.join(bundle_dir(), fn + '.png')

        # Save image file
        img.save(output)
        return output
