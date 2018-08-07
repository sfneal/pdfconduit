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
    return bundle_dir


def register_font(font='Vera.ttf'):
    """Register fonts for report labs canvas."""
    folder = bundle_dir() + os.sep + 'font'
    ttfFile = resource_path(os.path.join(folder, font))
    print(ttfFile)
    pdfmetrics.registerFont(TTFont("Vera", ttfFile))
    return ttfFile


FONT = register_font()
LETTER = letter[1], letter[0]
image_directory = str(bundle_dir() + os.sep + 'img')
