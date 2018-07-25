# Test encrypt module reliability
from pdfwatermarker import protect, secure, EncryptParams
import os
import shutil


def main():
    print('Testing encrypt module reliability')
    pdf = '/Users/Stephen/Desktop/20160054_FP.1.pdf'
    protected = '/Users/Stephen/Desktop/20160054_FP.1.pdf'
    secured = '/Users/Stephen/Desktop/20160054_FP.1.pdf'
    for f in [pdf, protected, secured]:
        try:
            os.remove(f)
        except FileNotFoundError:
            pass

    og = '/Volumes/Storage/HPA Design/Marketing Library/Floor Plan PDFs/20160054_FP.1.pdf'
    if os.path.exists(og):
        shutil.copy2(og, '/Users/Stephen/Desktop')

    if os.path.exists(pdf):
        owner_pw = 'foo'
        user_pw = 'baz'
        protect(pdf, user_pw, owner_pw)
        secure(pdf, user_pw, owner_pw)

        if os.path.exists(protected) and os.path.exists(secured):
            print('Success!')
        else:
            print('Failed!')
    else:
        print('Failed!')


if __name__ == '__main__':
    main()
