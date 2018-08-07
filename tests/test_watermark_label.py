import shutil
from pdfwatermarker.watermark.label import Label
from tests import pdf, directory


def main():
    print('Testing Watermark class reliability')
    label = 'test'
    l = Label(pdf, label).write()
    print(l)
    shutil.move(l, directory)


if __name__ == '__main__':
    main()
