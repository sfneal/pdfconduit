__all__ = ["upscale", "rotate", "Encrypt", "Merge", "Watermark", "Label", "WatermarkAdd", "slicer",
           "GUI"]
__version__ = '1.0.5'
__author__ = 'Stephen Neal'


from pdfwatermarker.utils import *
from pdfwatermarker.watermark import Watermark, Label, WatermarkAdd
from pdfwatermarker.upscale import upscale
from pdfwatermarker.rotate import rotate
from pdfwatermarker.encrypt import Encrypt
from pdfwatermarker.merge import Merge
from pdfwatermarker.slice import slicer
from pdfwatermarker.utils.gui import GUI
