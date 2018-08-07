from pdfwatermarker import Watermark, info
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

    security = info.security(encrypted, user_pw)

    try:
        # File checks
        assert os.path.exists(wtrmrk) is False
        assert os.path.exists(added) is True
        assert os.path.exists(encrypted) is True

        # Encryption checks
        assert info.encrypted(encrypted) is True
        assert security['/Length'] == 128
        assert security['/P'] == -1852
        print('Success!')
    except AssertionError:
        print('Failed!')


if __name__ == '__main__':
    main()
