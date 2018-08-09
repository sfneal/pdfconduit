import os
from pdfconduit.watermark import Label


def main():
    print('Testing Label reliability')
    pdf = 'data/charts.pdf'
    label = 'Last updated 7/10/18'
    l = Label(pdf, label).write()

    try:
        # File checks
        assert os.path.exists(l) is True
        os.remove(l)
        print('Success!')
    except AssertionError:
        print('Failed!')


if __name__ == '__main__':
    main()
