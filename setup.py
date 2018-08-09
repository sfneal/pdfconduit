from setuptools import setup, find_packages
from pdfwatermarker import __version__, __author__

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
        'looptools'
    ],
    include_package_data=True,
    url='https://github.com/mrstephenneal/pdfwatermarker',
    license='',
    author=__author__,
    author_email='stephen@hpadesign.com',
    description='PDF tool for watermarking, security and other utilities.',
    long_description='PDF watermark tool for internal use (HPA Design).'
)
