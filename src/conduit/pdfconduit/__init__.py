__all__ = []

__all__.extend(["upscale", "rotate", "Encrypt", "Merge", "Watermark", "Label", "WatermarkAdd", "slicer", "Info",
                "Flatten"])

try:
    from src.conduit.pdf import GUI
    GUI_INSTALLED = True
    __all__.extend("GUI")
except ImportError:
    GUI_INSTALLED = False
