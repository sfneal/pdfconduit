__all__ = ["set_destination", "resource_path", "write_pdf", "add_suffix", "open_window", "upscale", "rotate",
           "protect", "secure", "EncryptParams", "merge", "Watermark", "WatermarkGUI"]

import os
import sys
from pathlib import Path
from subprocess import call, Popen
from pdfwatermarker.write import write_pdf


def set_destination(source, suffix):
    """Create new pdf filename for temp files"""
    source_dirname = os.path.dirname(source)

    # Do not create nested temp folders (/temp/temp)
    if not source_dirname.endswith('temp'):
        directory = os.path.join(source_dirname, 'temp')  # directory
    else:
        directory = source_dirname

    # Create temp dir if it does not exist
    if not os.path.isdir(directory):
        os.mkdir(directory)

    # Parse source filename
    src_file_name = Path(source).stem  # file name
    src_file_ext = Path(source).suffix  # file extension

    # Concatenate new filename
    dst_path = src_file_name + '_' + suffix + src_file_ext
    return os.path.join(directory, dst_path)  # new full path


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


def add_suffix(file_path, suffix):
    """Adds suffix to a file name seperated by an underscore and returns file path."""
    split = os.path.basename(file_path).rsplit('.', 1)
    ext = split[1]
    name = split[0]
    out = name + '_' + suffix + '.' + ext
    return os.path.join(os.path.dirname(file_path), out)


def open_window(path):
    """Open path in finder or explorer window"""
    try:
        call(["open", "-R", str(Path(str(path)))])
    except FileNotFoundError:
        Popen(r'explorer /select,' + str(Path(str(path))))


from pdfwatermarker.upscale import upscale
from pdfwatermarker.rotate import rotate
from pdfwatermarker.encrypt import protect, secure, EncryptParams
from pdfwatermarker.merge import merge
from pdfwatermarker.watermark import Watermark, WatermarkGUI
