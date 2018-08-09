__all__ = ["upscale", "rotate", "Encrypt", "Merge", "Watermark", "Label", "WatermarkAdd", "slicer",
           "GUI"]
__version__ = '1.1.0'
__author__ = 'Stephen Neal'


from pdfconduit.utils import *
from pdfconduit.watermark import Watermark, Label, WatermarkAdd
from pdfconduit.upscale import upscale
from pdfconduit.rotate import rotate
from pdfconduit.encrypt import Encrypt
from pdfconduit.merge import Merge
from pdfconduit.slice import slicer
from pdfconduit.utils.gui import GUI
