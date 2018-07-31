import os
from pdfwatermarker.thirdparty.PyPDF2 import PdfFileReader
from pdfwatermarker import Watermark, EncryptParams, add_suffix, open_window
from looptools import ActiveTimer


def main():
    print('Testing Watermark class and secure function reliability')
    directory = '/Users/Stephen/Desktop'
    secure = os.path.join(directory, '20100141_Floor Plans_secured.pdf')
    if os.path.exists(secure):
        os.remove(secure)

    pdf = os.path.join(directory, '20100141_Floor Plans_compressed.pdf')
    project = '20160054'
    address = '43 Indian Lane'
    town = 'Franklin'
    state = 'MA'

    enc = EncryptParams('baz', 'foo', output=add_suffix(pdf, 'secured'))

    with ActiveTimer(Watermark):
        Watermark(pdf, project, address, town, state, encrypt=enc, encrypt_128=True)

    with open(secure, 'rb') as f:
        reader = PdfFileReader(f)
        if reader.isEncrypted:
            print('Encrypted:', os.path.basename(secure))

    if os.path.exists(secure):
        print('Success!')
        open_window(secure)
    else:
        print('Failed!')


if __name__ == '__main__':
    main()
