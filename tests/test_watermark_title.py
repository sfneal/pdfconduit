import os
from pdfwatermarker.watermark.watermark import Label
from tests import pdf, directory


def main():
    print('Testing Watermark class reliability')
    label = 'test'
    l = Label(pdf, label, title_page=True, output=os.path.join(directory, 'title.pdf')).watermark


if __name__ == '__main__':
    main()
