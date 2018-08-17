# Test encrypt module reliability
import os
from pdfconduit import Info, rotate
from tests import pdf


def main():
    print('Testing Rotate reliability')
    r = 90
    rotated1 = rotate(pdf, r, suffix='rotated_pypdf3', method='pypdf3')
    rotated2 = rotate(pdf, r, suffix='rotated_pdfrw', method='pdfrw')

    print(Info(rotated1).rotate)
    try:
        assert os.path.isfile(rotated1)
        assert Info(rotated1).rotate == r
        assert os.path.isfile(rotated2)
        assert Info(rotated1).rotate == r
        print('Success!', '\n')
    except AssertionError:
        print('Failed!')


if __name__ == '__main__':
    main()
