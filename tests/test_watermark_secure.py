import os
from pdfwatermarker import Watermark, EncryptParams, add_suffix, open_window
from looptools import ActiveTimer


def main():
    print('Testing Watermark class and secure function reliability')
    directory = '/Users/Stephen/Desktop'
    pdf = os.path.join(directory, '20180015(20170238) CDS(layered).pdf')

    project = '20160054'
    address = '43 Indian Lane'
    town = 'Franklin'
    state = 'MA'

    enc = EncryptParams('baz', 'foo', output=add_suffix(pdf, 'secured'))

    with ActiveTimer(Watermark):
        Watermark(pdf, project, address, town, state, encrypt=enc, encrypt_128=True)
    print('Success!')


if __name__ == '__main__':
    main()
