from pdfconduit import Watermark, Info
import os
from tests import pdf


def main():
    print('Testing Watermark draw, add and encrypt functionality')
    address = '43 Indian Lane'
    town = 'Franklin'
    state = 'MA'

    owner_pw = 'foo'
    user_pw = 'baz'

    w = Watermark(pdf, remove_temps=True, use_receipt=False)
    wtrmrk = w.draw(address, str(town + ', ' + state), opacity=0.08)
    added = w.add()
    encrypted = w.encrypt(user_pw, owner_pw)
    w.cleanup()

    security = Info(encrypted, user_pw).security

    try:
        # File checks
        assert os.path.exists(wtrmrk) is False
        assert os.path.exists(added) is True
        assert os.path.exists(encrypted) is True

        # Encryption checks
        assert Info(encrypted).encrypted is True
        assert security['/Length'] == 128
        # assert security['/P'] == -1852
        print('Success!')
        print('\n', security['/P'])
        print(Info(encrypted, user_pw).metadata)
    except AssertionError:
        print('Failed!')


if __name__ == '__main__':
    main()
