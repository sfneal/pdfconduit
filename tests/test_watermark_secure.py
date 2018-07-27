import os
from pdfwatermarker.thirdparty.PyPDF2 import PdfFileReader
from pdfwatermarker import Watermark, EncryptParams, add_suffix, open_window


def main():
    print('Testing Watermark class and secure function reliability')
    secure = '/Volumes/Storage/HPA Design/Marketing Library/Floor Plan PDFs/20160054_FP.1_secured.pdf'
    if os.path.exists(secure):
        os.remove(secure)

    pdf = '/Volumes/Storage/HPA Design/Marketing Library/Floor Plan PDFs/20160054_FP.1.pdf'
    project = '20160054'
    address = '43 Indian Lane'
    town = 'Franklin'
    state = 'MA'

    enc = EncryptParams('baz', 'foo', output=add_suffix(pdf, 'secured'))

    Watermark(pdf, project, address, town, state, encrypt=enc)

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
