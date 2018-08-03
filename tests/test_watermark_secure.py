from pdfwatermarker import Watermark, info
import os


def main():
    print('Testing Watermark class reliability')
    directory = '/Users/Stephen/Desktop/'

    pdf = os.path.join(directory, '20180053 CDs.pdf')
    address = '43 Indian Lane'
    town = 'Franklin'
    state = 'MA'

    w = Watermark(pdf, remove_temps=True)
    w.draw(address, str(town + ', ' + state), opacity=0.08)
    w.add()
    w.secure('', 'foo')
    wm = w.save()

    if os.path.exists(wm):
        print('Success!')


if __name__ == '__main__':
    main()
