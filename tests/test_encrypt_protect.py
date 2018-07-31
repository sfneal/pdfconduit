# Test encrypt module reliability
import os
from pdfwatermarker import protect, secure
from pdfwatermarker.utils import security_objects
from looptools import ActiveTimer


def main():
    print('Testing encrypt module reliability...')
    directory = '/Users/Stephen/Desktop'
    pdf = os.path.join(directory, '20180015(20170238) CDS(layered).pdf')

    if os.path.exists(pdf):
        owner_pw = 'foo'
        user_pw = 'baz'
        with ActiveTimer(protect):
            p = protect(pdf, user_pw, owner_pw, restrict_permission=True)
        print(p)
        print(security_objects(p))
        print('Success!')
    else:
        print('Failed!')


if __name__ == '__main__':
    main()
