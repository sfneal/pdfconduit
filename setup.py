from setuptools import setup, find_packages

setup(
    name='pdfwatermarker',
    version='0.1.8',
    packages=find_packages(),
    install_requires=[
        'pdfrw',
        'Pillow',
        'PyPDF2',
        'PySimpleGUI',
        'reportlab',
        'interruptingcow'
    ],
    include_package_data=True,
    url='https://github.com/mrstephenneal/pdfwatermarker',
    license='',
    author='Stephen Neal',
    author_email='stephen@hpadesign.com',
    description='Implemented resource_path function to find relative paths.',
    long_description='PDF watermark tool for internal use (HPA Design).'
)
