# Test encrypt module reliability
from pdfwatermarker import protect
from pdfwatermarker.utils import security_objects
import os


def main():
    print('Testing encrypt module reliability...')
    pdf = '/Users/Stephen/Desktop/20160054_FP.1.pdf'

    if os.path.exists(pdf):
        owner_pw = 'foo'
        user_pw = 'baz'
        p = protect(pdf, user_pw, owner_pw)
        print(p)
        print(security_objects(p))
        print('Success!')
    else:
        print('Failed!')


if __name__ == '__main__':
    main()
