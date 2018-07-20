from setuptools import setup, find_packages

setup(
    name='pdfwatermarker',
    version='0.1.4',
    packages=find_packages(),
    install_requires=[
        'pdfrw',
        'Pillow',
        'PyPDF2',
        'PySimpleGUI',
        'reportlab',
    ],
    include_package_data=True,
    url='https://github.com/mrstephenneal/pdfwatermarker',
    license='',
    author='Stephen Neal',
    author_email='stephen@hpadesign.com',
    description='Changed location of temp directory for dumping altered PDF files due to permissions related errors.',
    long_description='PDF watermark tool for internal use (HPA Design).'
)
