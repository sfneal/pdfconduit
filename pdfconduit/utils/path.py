# Set directory paths and file names
import os
import sys
from pathlib import Path
from typing import Optional

if "pathlib" in sys.modules:

    def _add_suffix(file_path: str, suffix: str, sep: str, ext: str):
        p = Path(file_path)
        _ext = p.suffix if ext is None else str("." + ext.strip("."))
        out = p.stem + sep + suffix + _ext  # p.suffix is file extension
        return os.path.join(os.path.dirname(file_path), out)

else:

    def _add_suffix(file_path: str, suffix: str, sep: str, ext: str):
        split = os.path.basename(file_path).rsplit(".", 1)
        ext = split[1] if ext is None else str("." + ext.strip("."))
        return os.path.join(
            os.path.dirname(file_path), split[0] + sep + suffix + "." + ext
        )


def add_suffix(
    file_path: str, suffix: str = "modified", sep: str = "_", ext: Optional[str] = None
):
    """Adds suffix to a file name seperated by an underscore and returns file path."""
    return _add_suffix(file_path, suffix, sep, ext)