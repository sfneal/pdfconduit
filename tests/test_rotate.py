# Test encrypt module reliability
import os
from pdfconduit import info, rotate
from tests import pdf


def main():
    print('Testing Rotate reliability')
    r = 90
    rotated1 = rotate(pdf, r, suffix='rotated_pypdf3', method='pypdf3')
    rotated2 = rotate(pdf, r, suffix='rotated_pdfrw', method='pdfrw')

    print(info.rotate(rotated1))
    try:
        assert os.path.isfile(rotated1)
        assert info.rotate(rotated1) == r
        assert os.path.isfile(rotated2)
        assert info.rotate(rotated2) == r
        print('Success!', '\n')
    except AssertionError:
        print('Failed!')


if __name__ == '__main__':
    main()
