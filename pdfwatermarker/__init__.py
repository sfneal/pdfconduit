__all__ = ["set_destination", "resource_path", "overlay_pdfs", "add_suffix", "open_window", "upscale", "rotate",
           "protect", "secure", "EncryptParams", "merge", "Watermark", "WatermarkGUI"]
__version__ = '1.0.0'
__author__ = 'Stephen Neal'


from pdfwatermarker.utils import *
from pdfwatermarker.upscale import upscale
from pdfwatermarker.rotate import rotate
from pdfwatermarker.encrypt import protect, secure, EncryptParams
from pdfwatermarker.merge import merge
from pdfwatermarker.watermark import Watermark, WatermarkGUI
