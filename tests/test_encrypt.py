# Test encrypt module reliability
from pdfwatermarker import protect, secure, EncryptParams
import os
import shutil


def main():
    print('Testing encrypt module reliability')
    pdf = '/Users/Stephen/Desktop/20160054_FP.1.pdf'

    og = '/Volumes/Storage/HPA Design/Marketing Library/Floor Plan PDFs/20160054_FP.1.pdf'
    if os.path.exists(og):
        shutil.copy2(og, '/Users/Stephen/Desktop')

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
