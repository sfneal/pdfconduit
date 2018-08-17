import os
from pdfconduit import Watermark
from tests import pdf


def main():
    print('Testing Watermark draw and add functionality')
    address = '43 Indian Lane'
    town = 'Franklin'
    state = 'MA'

    w1 = Watermark(pdf, use_receipt=False)
    wtrmrk1 = w1.draw(address, str(town + ', ' + state))
    added1 = w1.add(suffix='watermarked_overlay')

    w2 = Watermark(pdf, use_receipt=False)
    wtrmrk2 = w2.draw(address, str(town + ', ' + state))
    added2 = w2.add(underneath=True, suffix='watermarked_underneath')

    w1.cleanup()

    try:
        # File checks
        assert os.path.exists(wtrmrk1) is False
        assert os.path.exists(wtrmrk2) is False
        assert os.path.exists(added1) is True
        assert os.path.exists(added2) is True
        print('Success!')
    except AssertionError:
        print('Failed!')


if __name__ == '__main__':
    main()
