# View directories and files in a window
from pathlib import Path
from subprocess import call, Popen
from sys import modules


def open_window(path):
    """Open path in finder or explorer window"""
    if 'pathlib' in modules:
        try:
            call(["open", "-R", str(Path(str(path)))])
        except FileNotFoundError:
            Popen(r'explorer /select,' + str(Path(str(path))))
    else:
        print('pathlib module must be installed to execute open_window function')
