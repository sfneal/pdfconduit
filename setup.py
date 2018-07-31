from setuptools import setup, find_packages

setup(
    name='pdfwatermarker',
    version='0.2.1',
    packages=find_packages(),
    install_requires=[
        'pdfrw',
        'Pillow',
        'PySimpleGUI',
        'reportlab',
        'looptools'
    ],
    include_package_data=True,
    url='https://github.com/mrstephenneal/pdfwatermarker',
    license='',
    author='Stephen Neal',
    author_email='stephen@hpadesign.com',
    description='PDF tool for watermarking, security and other utilities.',
    long_description='PDF watermark tool for internal use (HPA Design).'
)
