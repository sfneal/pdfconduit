# Test encrypt module reliability
import os
from pdfconduit import Info, upscale
from tests import pdf


# def calc_scale()


def main():
    print('Testing Rotate reliability')
    s = 2.0
    upscale1 = upscale(pdf, scale=s)

    print('PDF - old:', Info(pdf).size)
    print('PDF - new:', Info(upscale1).size)

    try:
        assert os.path.isfile(upscale1)
        assert Info(upscale1).size == tuple([i * s for i in Info(pdf).size])
        print('Success!', '\n')
    except AssertionError:
        print('Failed!')


if __name__ == '__main__':
    main()
