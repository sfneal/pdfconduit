from tests import *


def main():
    functions = [test_encrypt, test_merge, test_watermark, test_watermark_label, test_watermark_encrypt,
                 test_watermark_flat]

    for func in functions:
        func.main()
        print('\n')


if __name__ == '__main__':
    main()
