from pdfwatermarker import Watermark
import os


def main():
    print('Testing Watermark class reliability')
    # watermark = '/Volumes/Storage/HPA Design/Marketing Library/Floor Plan PDFs/20160018_FP.1_watermarked.pdf'
    watermark = '/Users/Stephen/Desktop/20100141_Floor Plans_watermarked.pdf'
    if os.path.exists(watermark):
        os.remove(watermark)
    
    # pdf = '/Volumes/Storage/HPA Design/Marketing Library/Floor Plan PDFs/20160018_FP.1.pdf'
    pdf = '/Users/Stephen/Desktop/20100141_Floor Plans.pdf'
    project = '20160054'
    address = '43 Indian Lane'
    town = 'Franklin'
    state = 'MA'
    
    Watermark(pdf, project, address, town, state, opacity=0.08, remove_temps=False)

    if os.path.exists(watermark):
        print('Success!')
    else:
        print('Failed!')


if __name__ == '__main__':
    main()
