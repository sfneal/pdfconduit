__all__ = ["set_destination", "resource_path", "write_pdf", "add_suffix", "upscale", "rotate", "Watermark",
           "WatermarkGUI"]

import os
from pathlib import Path
import sys

from pdfwatermarker.write import write_pdf


def set_destination(source, suffix):
    # Create new pdf filename
    directory = os.path.join(os.path.dirname(source), 'temp')  # directory
    if not os.path.isdir(directory):
        os.mkdir(directory)
    src_file_name = Path(source).stem  # file name
    src_file_ext = Path(source).suffix  # file extension
    dst_path = src_file_name + '_' + suffix + src_file_ext  # new concatenated file name
    return os.path.join(directory, dst_path)  # new full path


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


def add_suffix(file_path, suffix):
    split = os.path.basename(file_path).rsplit('.', 1)
    ext = split[1]
    name = split[0]
    out = name + '_' + suffix + '.' + ext
    return os.path.join(os.path.dirname(file_path), out)

from pdfwatermarker.upscale import upscale
from pdfwatermarker.rotate import rotate
from pdfwatermarker.watermark import Watermark, WatermarkGUI
