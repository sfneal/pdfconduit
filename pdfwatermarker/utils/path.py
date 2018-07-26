# Set directory paths and file names
import os
import sys
from pathlib import Path


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
    """Adjust path for executable use in executable file"""
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
