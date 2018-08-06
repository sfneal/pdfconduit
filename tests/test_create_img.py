import os
import shutil
from pdfwatermarker.watermark.watermark import Watermark
from tests import directory, pdf


def main():
    print('Testing Watermark class flatten reliability')

    address = '43 Indian Lane'
    town = 'Franklin'
    state = 'MA'

    w = Watermark(pdf, remove_temps=True, use_receipt=False)
    flat = w.draw(address, str(town + ', ' + state), opacity=0.08, flatten=True)
    layered = w.draw(address, str(town + ', ' + state), opacity=0.08, flatten=False)
    shutil.move(flat, os.path.join(directory, 'flat.pdf'))
    shutil.move(layered, os.path.join(directory, 'layered.pdf'))
    wm = w.cleanup()

    if os.path.exists(wm):
        print('Success!')


if __name__ == '__main__':
    main()
