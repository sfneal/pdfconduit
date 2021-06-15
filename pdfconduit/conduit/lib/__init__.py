import os
from PyBundle import bundle_dir, resource_path


def _image_directory():
    directory = os.path.join(bundle_dir(), 'img')
    if os.path.exists(directory):
        return directory
    else:
        print(directory, 'can not be found')


IMAGE_DIRECTORY = _image_directory()


def available_images():
    imgs = [i for i in os.listdir(IMAGE_DIRECTORY) if not i.startswith('.')]
    if len(imgs) > 0:
        return sorted(imgs, reverse=True)
    else:
        return ['Add images...']


IMAGE_DEFAULT = resource_path('Wide.png')


__all__ = ['IMAGE_DEFAULT', 'IMAGE_DIRECTORY', 'available_images']