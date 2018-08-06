# Test encrypt module reliability
import os
from pdfwatermarker import protect
from pdfwatermarker.utils import info
from looptools import ActiveTimer
from . import directory, pdf


def main():
    print('Testing encrypt module reliability...')
    if os.path.exists(pdf):
        owner_pw = 'foo'
        user_pw = 'baz'
        with ActiveTimer(protect):
            p = protect(pdf, user_pw, owner_pw)
            s = info.security(p, user_pw)
            for k, v in s:
                print("{0:20} ---> {1}".format(k, v))
        print('Success!')
    else:
        print('Failed!')


if __name__ == '__main__':
    main()
