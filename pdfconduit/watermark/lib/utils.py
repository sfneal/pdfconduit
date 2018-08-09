import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
from pdfconduit.utils import resource_path, bundle_dir


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


def available_images():
    return sorted([i for i in os.listdir(IMAGE_DIRECTORY) if not i.startswith('.')], reverse=True)


FONT = register_font()
LETTER = letter[1], letter[0]
IMAGE_DIRECTORY = _image_directory()
IMAGE_DEFAULT = resource_path('Wide.png')
