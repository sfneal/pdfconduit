from pdfwatermarker import Watermark, info
import os


def main():
    print('Testing Watermark class reliability')
    directory = '/Users/Stephen/Desktop/'

    pdf = os.path.join(directory, '20110055_FP.1.pdf')
    project = '20160054'
    address = '43 Indian Lane'
    town = 'Franklin'
    state = 'MA'
    
    wm = str(Watermark(pdf, project, address, town, state, opacity=0.08, remove_temps=False))

    if os.path.exists(wm):
        print('Success!')


if __name__ == '__main__':
    main()
