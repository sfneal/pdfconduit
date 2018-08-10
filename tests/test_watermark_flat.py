import os
import shutil
from pdfconduit import Watermark
from tests import pdf, directory
import filecmp


def main():
    print('Testing Watermark draw, add and encrypt functionality')
    address = '43 Indian Lane'
    town = 'Franklin'
    state = 'MA'

    w = Watermark(pdf, remove_temps=True, use_receipt=False)
    flat = w.draw(address, str(town + ', ' + state), opacity=0.08, flatten=True)
    layered = w.draw(address, str(town + ', ' + state), opacity=0.08, flatten=False)

    try:
        # File checks
        assert os.path.exists(flat) is True
        assert os.path.exists(layered) is True
        assert filecmp.cmp(flat, layered) is False
        shutil.move(flat, os.path.join(directory, 'flat.pdf'))
        shutil.move(layered, os.path.join(directory, 'layered.pdf'))
        w.cleanup()
        print('Success!')
    except AssertionError:
        print('Failed!')


if __name__ == '__main__':
    main()
