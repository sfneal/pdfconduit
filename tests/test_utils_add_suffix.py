import os
from pdfconduit.utils.path import add_suffix
from tests import pdf


def main():
    print('Testing add_suffix function reliability:')

    print('\nDirectory:')
    print(os.path.dirname(pdf))

    print('\nOriginal Filename:')
    print(os.path.basename(pdf))

    print('\nNew Filename:')
    print(os.path.basename(add_suffix(pdf, 'modified')))


if __name__ == '__main__':
    main()
