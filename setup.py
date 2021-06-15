import os
from setuptools import setup, find_packages

long_description = """
A Pure-Python library built as a PDF toolkit.  Prepare documents for distribution.

Features:
- Watermark: Dynamically generate watermarks and add watermark to existing document
- Label: Overlay text labels such as filename or date to documents 
- Encrypt: Password protect and restrict permissions to print only
- Rotate: Rotate by increments of 90 degrees
- Upscale: Scale PDF size
- Merge: Concatenate multiple documents into one file
- Slice: Extract page ranges from documents
- Extract Text and Images
- Retrieve document metadata and information
"""


def get_version(version_file='_version.py'):
    """Retrieve the package version from a version file in the package root."""
    filename = os.path.join(os.path.dirname(__file__), 'pdfconduit', version_file)
    with open(filename, 'rb') as fp:
        return fp.read().decode('utf8').split('=')[1].strip(" \n'")


setup(
    name='pdfconduit',
    version=get_version(),
    packages=find_packages(),
    namespace_packages=['pdf'],
    install_requires=[
        'looptools',
        'pdfconduit-convert>=1.2.8',
        'pdfconduit-modify>=2.2.4',
        'pdfconduit-transform>=1.2.2',
        'pdfconduit-utils>=1.1.2',
    ],
    include_package_data=True,
    url='https://github.com/sfneal/pdfconduit',
    license='',
    author='Stephen Neal',
    author_email='stephen@stephenneal.net',
    description='PDF toolkit for preparing documents for distribution.',
    long_description=long_description,
)
