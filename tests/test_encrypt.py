# Test encrypt module reliability
from pdfwatermarker import encrypt
import os
from . import directory, pdf


def main():
    print('Testing encrypt module reliability')

    if os.path.exists(pdf):
        user_pw = 'baz'
        owner_pw = 'foo'
        encrypt(pdf, user_pw, owner_pw)
        print('Success!')
    else:
        print('Failed!')


if __name__ == '__main__':
    main()
