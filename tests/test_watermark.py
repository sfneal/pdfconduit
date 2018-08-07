from pdfwatermarker import Watermark
import os
from tests import pdf


def main():
    print('Testing Watermark draw, add and encrypt functionality')
    address = '43 Indian Lane'
    town = 'Franklin'
    state = 'MA'

    w = Watermark(pdf, remove_temps=True, use_receipt=False)
    wtrmrk = w.draw(address, str(town + ', ' + state), opacity=0.08)
    added = w.add()
    w.cleanup()

    try:
        # File checks
        assert os.path.exists(wtrmrk) is False
        assert os.path.exists(added) is True
        print('Success!')
    except AssertionError:
        print('Failed!')


if __name__ == '__main__':
    main()
