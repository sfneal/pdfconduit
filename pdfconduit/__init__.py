__all__ = ["Encrypt", "Merge", "Watermark", "Label", "WatermarkAdd", "Info"]

from pdf.conduit import *

try:
    from pdf.gui.gui import GUI
    GUI_INSTALLED = True
    __all__.append("GUI")
except ImportError:
    GUI_INSTALLED = False


try:
    from pdf.modify import upscale, rotate, slicer
    MODIFY_INSTALLED = True
    __all__.extend(["slicer", "upscale", "rotate"])
except ImportError:
    MODIFY_INSTALLED = False


try:
    from pdf.convert import Flatten
    MODIFY_INSTALLED = True
    __all__.append("Flatten")
except ImportError:
    MODIFY_INSTALLED = False
