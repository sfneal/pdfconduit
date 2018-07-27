# Test encrypt module reliability
import os
from pdfwatermarker import protect
from pdfwatermarker.utils import security_objects
from looptools import ActiveTimer


def main():
    print('Testing encrypt module reliability...')
    pdf = '/Volumes/Storage/HPA Design/Marketing Library/Floor Plan PDFs/20160054_FP.1.pdf'

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
