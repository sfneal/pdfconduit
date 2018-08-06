from pdfwatermarker.watermark.watermark import Label
from tests import pdf


def main():
    print('Testing Watermark class reliability')
    label = 'test'
    l = Label(pdf, label).write()


if __name__ == '__main__':
    main()
