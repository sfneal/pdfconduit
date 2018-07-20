from setuptools import setup, find_packages

setup(
    name='pdfwatermarker',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'pdfrw',
        'Pillow',
        'PyPDF2',
        'PySimpleGUI',
        'reportlab',
    ],
    url='https://github.com/mrstephenneal/pdfwatermarker',
    license='',
    author='Stephen Neal',
    author_email='stephen@hpadesign.com',
    description='PDF watermark tool for internal use (HPA Design).',
    long_description='PDF watermark tool for internal use (HPA Design).'
)
