# Test encrypt module reliability
import os
from pdfconduit import Encrypt, Info
from tests import pdf, directory
from looptools import ActiveTimer


def main():
    print('Testing Encrypt reliability')
    owner_pw = 'foo'
    user_pw = 'baz'

    _range = [-(x + 50) for x in range(0, 1852)[::100]]
    print(_range)
    for i in _range:
        with ActiveTimer(i):
            p = Encrypt(pdf, user_pw, owner_pw, output=os.path.join(directory, 'P', str(i) + '.pdf'),
                        overwrite_permission=i)
            security = Info(p.output, user_pw).security

            try:
                assert Info(p.output, user_pw).encrypted is True
                assert security['/Length'] == 128
                assert security['/P'] == i
                print('Success!', '\n')
            except AssertionError:
                print('Failed!')
                print(security)


if __name__ == '__main__':
    main()
