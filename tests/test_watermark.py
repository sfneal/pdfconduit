from pdfwatermarker import Watermark
import os


def main():
    print('Testing Watermark class reliability')
    watermark = '/Volumes/Storage/HPA Design/Marketing Library/Floor Plan PDFs/20160054_FP.1_watermarked.pdf'
    if os.path.exists(watermark):
        os.remove(watermark)
    
    pdf = '/Volumes/Storage/HPA Design/Marketing Library/Floor Plan PDFs/20160054_FP.1.pdf'
    project = '20160054'
    address = '43 Indian Lane'
    town = 'Franklin'
    state = 'MA'
    
    Watermark(pdf, project, address, town, state)

    if os.path.exists(watermark):
        print('Success!')
    else:
        print('Failed!')


if __name__ == '__main__':
    main()
