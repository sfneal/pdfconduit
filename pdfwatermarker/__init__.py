__all__ = ["upscale", "rotate", "protect", "Merge", "Watermark", "WatermarkGUI", "slicer"]
__version__ = '1.0.2'
__author__ = 'Stephen Neal'


from pdfwatermarker.utils import *
from pdfwatermarker.watermark import Watermark, WatermarkGUI
from pdfwatermarker.upscale import upscale
from pdfwatermarker.rotate import rotate
from pdfwatermarker.encrypt import protect
from pdfwatermarker.merge import Merge
from pdfwatermarker.slice import slicer
