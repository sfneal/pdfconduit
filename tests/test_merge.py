import os
from pdfconduit import Merge, Info
from tests import directory


def main():
    print('Testing Merge reliability')
    pdfs = [os.path.join(directory, p) for p in ['article.pdf', 'charts.pdf', 'document.pdf', 'manual.pdf']]

    # Merge PDF files
    m = Merge(pdfs)

    try:
        assert os.path.exists(m.file) is True
        assert sum([Info(pdf).pages for pdf in pdfs]) == Info(m.file).pages
        print('Success!')
    except AssertionError:
        print('Failed!')


if __name__ == "__main__":
    # calling the main function
    main()
