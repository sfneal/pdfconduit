# Set directory paths and file names
import os
from pathlib import Path
from typing import Optional


def add_suffix(
    file_path: str, suffix: str = "modified", sep: str = "_", ext: Optional[str] = None
):
    """Adds suffix to a file name seperated by an underscore and returns file path."""
    p = Path(file_path)
    _ext = p.suffix if ext is None else str("." + ext.strip("."))
    out = p.stem + sep + suffix + _ext  # p.suffix is file extension
    return os.path.join(os.path.dirname(file_path), out)
