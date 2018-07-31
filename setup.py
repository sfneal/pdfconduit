from setuptools import setup, find_packages

setup(
    name='pdfwatermarker',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        'pdfrw',
        'Pillow',
        'PyPDF2==1.26.0',
        'PySimpleGUI',
        'reportlab',
        'looptools'
    ],
    include_package_data=True,
    url='https://github.com/mrstephenneal/pdfwatermarker',
    license='',
    author='Stephen Neal',
    author_email='stephen@hpadesign.com',
    description='Implemented resource_path function to find relative paths.',
    long_description='PDF watermark tool for internal use (HPA Design).'
)
