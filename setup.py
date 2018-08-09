from setuptools import setup, find_packages
from pdfconduit import __version__, __author__

long_description = """
A Pure-Python library built as a PDF toolkit.  It was developed to prepare documents for distribution.

- Watermark
    - Dynamically generate watermarks
    - Add watermark to existing document
- Label
    - Overlay text labels such as filename or date to documents
    - Add title page to document 
- Encrypt
    - Password protect
    - Restrict permissions to print only
- Rotate 
    - By increments of 90 degrees
- Upscale
- Merge
    - Concatenate multiple documents into one file
- Slice
    - Extract page ranges from documents
- Extract Text and Images
- Retrieve document metadata and information
"""

setup(
    name='pdfwatermarker',
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'pdfrw',
        'PyPDF3',
        'Pillow',
        'PySimpleGUI',
        'reportlab',
        'looptools',
        'tqdm'
    ],
    include_package_data=True,
    url='https://github.com/mrstephenneal/pdfconduit',
    license='',
    author=__author__,
    author_email='stephen@stephenneal.net',
    description='PDF toolkit for preparing documents for distribution.',
    long_description=long_description,
)
