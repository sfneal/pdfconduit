__all__ = []


# Conduit installation
try:
    from pdf.conduit import Encrypt, Watermark, Label, WatermarkAdd
    CONDUIT_INSTALL = True
    __all__.extend(["Encrypt", "Watermark", "Label", "WatermarkAdd"])
except ImportError:
    CONDUIT_INSTALL = False


# Utils installation
try:
    from pdf.utils.info import Info
    UTILS_INSTALL = True
    __all__.extend(["Info"])
except ImportError:
    UTILS_INSTALL = False


# GUI installation
try:
    from pdf.gui.gui import GUI
    GUI_INSTALLED = True
    __all__.extend(["GUI"])
except ImportError:
    GUI_INSTALLED = False


# Transform installation
try:
    from pdf.transform import upscale, rotate, slicer, Merge
    MODIFY_INSTALLED = True
    __all__.extend(["slicer", "upscale", "rotate", "Merge"])
except ImportError:
    MODIFY_INSTALLED = False


# Convert installation
try:
    from pdf.convert import Flatten
    CONVERT_INSTALLED = True
    __all__.extend(["Flatten"])
except ImportError:
    CONVERT_INSTALLED = False
