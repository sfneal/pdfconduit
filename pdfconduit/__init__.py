from ._version import __author__, __version__
from .utils import *
from .watermark import Watermark, Label, WatermarkAdd
from .upscale import upscale
from .rotate import rotate
from .encrypt import Encrypt
from .merge import Merge
from .slice import slicer
from .flatten import Flatten
from .utils.gui import GUI


__all__ = ["upscale", "rotate", "Encrypt", "Merge", "Watermark", "Label", "WatermarkAdd", "slicer",
           "GUI", "Info", "Flatten"]
__version__ = __version__
__author__ = __author__
