# Add, remove and view images in the GUI library
import os
import shutil
from pathlib import Path

GUI_ROOT = os.path.dirname(os.path.dirname(__file__))
IMG_DIR = os.path.join(GUI_ROOT, 'lib', 'img')
IMAGES = os.listdir(IMG_DIR)


def add(image_path, file_name=None):
    """Add an image to the GUI img library."""
    if file_name is not None:
        dst_path = os.path.join(IMG_DIR, str(Path(file_name).stem + Path(image_path).suffix))
    else:
        dst_path = IMG_DIR

    if os.path.isfile(image_path):
        shutil.copy2(image_path, dst_path)


def remove(image):
    """Remove an image to the GUI img library."""
    path = os.path.join(IMG_DIR, image)
    if os.path.isfile(path):
        os.remove(path)


def view(gui=False):
    """
    Return a list of available images and
    launch GUI window to view images if GUI is true.
    """
    # TODO: write function
    pass
