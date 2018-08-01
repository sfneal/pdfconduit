import os
from pdfwatermarker import Watermark, EncryptParams, add_suffix, info
from looptools import ActiveTimer


def main():
    print('Testing Watermark class and secure function reliability')

    directory = '/Users/Stephen/Desktop'
    filename = '20150094_Market Model.pdf'

    pdf = os.path.join(directory, filename)
    project = '20160054'
    address = '43 Indian Lane'
    town = 'Franklin'
    state = 'MA'

    user_pw = 'baz'
    owner_pw = 'foo'

    enc = EncryptParams(user_pw, owner_pw, output=add_suffix(pdf, 'secured'))
    with ActiveTimer(Watermark):
        secured = Watermark(pdf, project, address, town, state, encrypt=enc, encrypt_128=True)

    print(info.metadata(str(secured), user_pw))
    print(info.security(str(secured), user_pw))
    print('Success!')


if __name__ == '__main__':
    main()
