__all__ = ["upscale", "rotate", "Encrypt", "Merge", "Watermark", "Label", "WatermarkAdd", "slicer", "Info", "Flatten"]

from src.conduit.pdf.conduit import *

try:
    from src.gui.pdf.gui.gui import GUI
    GUI_INSTALLED = True
    __all__.extend("GUI")
except ImportError:
    GUI_INSTALLED = False
