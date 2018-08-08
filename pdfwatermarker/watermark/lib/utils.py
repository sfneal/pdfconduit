import os
import sys
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
from pdfwatermarker.utils import resource_path


def bundle_dir():
    """Handle resource management within an executable file."""
    if getattr(sys, 'frozen', False):
        # we are running in a bundle
        bundle_dir = sys._MEIPASS
    else:
        # we are running in a normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(bundle_dir):
        return bundle_dir


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


FONT = register_font()
LETTER = letter[1], letter[0]
image_directory = _image_directory()
