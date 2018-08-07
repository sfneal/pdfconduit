# Test encrypt module reliability
from pdfwatermarker import Encrypt
from pdfwatermarker.utils import info
from tests import pdf


def main():
    print('Testing encrypt module reliability...')
    owner_pw = 'foo'
    user_pw = 'baz'

    p = Encrypt(pdf, user_pw, owner_pw)

    security = info.security(p.output, user_pw)

    try:
        assert security['/Length'] == 128
        assert security['/P'] == -1852
        print('Success!')
    except AssertionError:
        print('Failed!')


if __name__ == '__main__':
    main()
