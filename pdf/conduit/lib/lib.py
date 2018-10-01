import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PyBundle import bundle_dir, resource_path


def register_font(font='Vera.ttf'):
    """Register fonts for report labs canvas."""
    directory = os.path.join(bundle_dir(), 'font')
    ttfFile = resource_path(os.path.join(directory, font))
    if os.path.exists(ttfFile):
        pdfmetrics.registerFont(TTFont("Vera", ttfFile))
        return ttfFile
    else:
        print(ttfFile, 'can not be found')


def _image_directory():
    directory = os.path.join(bundle_dir(), 'img')
    if os.path.exists(directory):
        return directory
    else:
        print(directory, 'can not be found')


IMAGE_DIRECTORY = _image_directory()


def available_images():
    imgs = [i for i in os.listdir(IMAGE_DIRECTORY) if not i.startswith('.')]
    if len(imgs) > 0:
        return sorted(imgs, reverse=True)
    else:
        return ['Add images...']


FONT = register_font()
IMAGE_DEFAULT = resource_path('Wide.png')
