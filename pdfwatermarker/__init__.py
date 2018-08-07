__all__ = ["upscale", "rotate", "encrypt", "Merge", "Watermark", "WatermarkGUI", "Label", "WatermarkAdd", "slicer"]
__version__ = '1.0.3'
__author__ = 'Stephen Neal'


from pdfwatermarker.utils import *
from pdfwatermarker.watermark import Watermark, WatermarkGUI, Label, WatermarkAdd
from pdfwatermarker.upscale import upscale
from pdfwatermarker.rotate import rotate
from pdfwatermarker.encrypt import encrypt
from pdfwatermarker.merge import Merge
from pdfwatermarker.slice import slicer
