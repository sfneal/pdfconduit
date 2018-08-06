# Test encrypt module reliability
from pdfwatermarker import protect
import os
from . import directory, pdf


def main():
    print('Testing encrypt module reliability')

    if os.path.exists(pdf):
        owner_pw = 'foo'
        user_pw = 'baz'
        protect(pdf, user_pw, owner_pw)
        print('Success!')
    else:
        print('Failed!')


if __name__ == '__main__':
    main()
