# Set directory paths and file names
import os
import sys
from pathlib import Path


def set_destination(source, suffix, filename=False, ext=None):
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
    if filename:
        src_file_name = filename
    else:
        src_file_name = Path(source).stem  # file name
    if ext:
        src_file_ext = ext
    else:
        src_file_ext = Path(source).suffix  # file extension

    # Concatenate new filename
    dst_path = src_file_name + '_' + suffix + src_file_ext
    full_path = os.path.join(directory, dst_path)  # new full path

    if not os.path.exists(full_path):
        return full_path
    else:
        # If file exists, increment number until filename is unique
        number = 1
        while True:
            dst_path = src_file_name + '_' + suffix + '_' + str(number) + src_file_ext
            if not os.path.exists(dst_path):
                break
            number = number + 1
        full_path = os.path.join(directory, dst_path)  # new full path
        return full_path


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
