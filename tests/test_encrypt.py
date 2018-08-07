# Test encrypt module reliability
from pdfwatermarker import Encrypt
import os
from tests import directory, pdf


def main():
    print('Testing encrypt module reliability')

    if os.path.exists(pdf):
        user_pw = 'baz'
        owner_pw = 'foo'
        Encrypt(pdf, user_pw, owner_pw)
        print('Success!')
    else:
        print('Failed!')


if __name__ == '__main__':
    main()
