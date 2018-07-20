__all__ = ["set_destination", "upscale", "rotate", "Watermark"]

import os
from pathlib import Path


def set_destination(source, suffix):
    # Create new pdf filename
    directory = os.path.join(os.path.dirname(__file__), 'watermark' + os.sep + 'lib' + os.sep + 'temp')  # directory
    if not os.path.isdir(directory):
        os.mkdir(directory)
    src_file_name = Path(source).stem  # file name
    src_file_ext = Path(source).suffix  # file extension
    dst_path = src_file_name + '_' + suffix + src_file_ext  # new concatenated file name
    return os.path.join(directory, dst_path)  # new full path


from pdfwatermarker.upscale import upscale
from pdfwatermarker.rotate import rotate
from pdfwatermarker.watermark import Watermark
