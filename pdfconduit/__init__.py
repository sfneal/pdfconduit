__all__ = []

from pdfconduit.conduit import *
from pdfconduit._version import __author__, __version__

__all__.extend(["upscale", "rotate", "Encrypt", "Merge", "Watermark", "Label", "WatermarkAdd", "slicer", "Info",
                "Flatten"])

try:
    from pdfconduit.gui import GUI
    GUI_INSTALLED = True
    __all__.extend("GUI")
except ImportError:
    GUI_INSTALLED = False


__version__ = __version__
__author__ = __author__
