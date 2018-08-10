import os
from pdfconduit.utils.extract import img_extract, text_extract
from tests import directory


def main():
    pdf = os.path.join(directory, 'workbook.pdf')
    img_extract(pdf)
    print(text_extract(pdf))


if __name__ == '__main__':
    main()
