import os
from typing import List

from PyBundle import bundle_dir, resource_path


def _image_directory() -> str:
    directory = os.path.join(bundle_dir(), "img")
    if os.path.exists(directory):
        return directory
    else:
        raise Exception("No image directory found")


IMAGE_DIRECTORY = _image_directory()


def available_images() -> List[str]:
    images = [i for i in os.listdir(IMAGE_DIRECTORY) if not i.startswith(".")]
    if len(images) > 0:
        return sorted(images, reverse=True)
    else:
        return []


IMAGE_DEFAULT = resource_path("watermark.png")

__all__ = ["IMAGE_DEFAULT", "IMAGE_DIRECTORY", "available_images"]
