from pdfwatermarker import Watermark, info
import os
from . import directory, pdf


def main():
    print('Testing Watermark class reliability')
    address = '43 Indian Lane'
    town = 'Franklin'
    state = 'MA'

    w = Watermark(pdf, remove_temps=True)
    w.draw(address, str(town + ', ' + state), opacity=0.08)
    w.add()
    w.encrypt('', 'foo')
    wm = w.cleanup()

    if os.path.exists(wm):
        print('Success!')


if __name__ == '__main__':
    main()
