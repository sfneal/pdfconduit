from pdfwatermarker.watermark.draw import TextDraw
import os
import shutil
from tqdm import tqdm


def main():
    print('Testing Watermark class reliability')
    directory = '/Users/Stephen/Desktop/'

    pdf = os.path.join(directory, '20150094_Market Model.pdf')
    text = os.path.basename(pdf)
    t = TextDraw(pdf, text, output_overwrite=True)


if __name__ == '__main__':
    main()
