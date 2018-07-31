# Test encrypt module reliability
from pdfwatermarker import protect, secure, EncryptParams
import os
import shutil


def main():
    print('Testing encrypt module reliability')
    directory = '/Users/Stephen/Desktop'
    pdf = os.path.join(directory, '20100141_Floor Plans.pdf')

    if os.path.exists(pdf):
        owner_pw = 'foo'
        user_pw = 'baz'
        protect(pdf, user_pw, owner_pw)
        secure(pdf, user_pw, owner_pw)
        print('Success!')
    else:
        print('Failed!')

if __name__ == '__main__':
    main()
