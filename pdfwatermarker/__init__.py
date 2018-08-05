__all__ = ["set_destination", "resource_path", "overlay_pdfs", "add_suffix", "open_window", "upscale", "rotate",
           "protect", "secure", "Merge", "Watermark", "WatermarkGUI", "slicer"]
__version__ = '1.0.1'
__author__ = 'Stephen Neal'


from pdfwatermarker.utils import *
from pdfwatermarker.watermark import Watermark, WatermarkGUI
from pdfwatermarker.upscale import upscale
from pdfwatermarker.rotate import rotate
from pdfwatermarker.encrypt import protect, secure
from pdfwatermarker.merge import Merge
from pdfwatermarker.slice import slicer
