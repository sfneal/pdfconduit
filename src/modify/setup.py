import re
from setuptools import setup, find_packages

long_description = """
PDF modification package
"""

# Retrieve version number
VERSIONFILE = "pdf/modify/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE))

setup(
    install_requires=[
        'reportlab>=3.5.13',
        'pdfrw>=0.4',
        'Pillow>=5.4.1',
        'pdfconduit-utils>=1.0.4',
    ],
    name='pdfconduit-modify',
    version=verstr,
    packages=find_packages(),
    namespace_packages=['pdf'],
    include_package_data=True,
    url='https://github.com/mrstephenneal/pdfconduit',
    license='',
    author='Stephen Neal',
    author_email='stephen@stephenneal.net',
    description='PDF toolkit for preparing documents for distribution.',
    long_description=long_description,
)
