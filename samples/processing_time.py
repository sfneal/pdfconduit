from time import time

from looptools import Timer

from pdfconduit import Pdfconduit
from tests import test_data_path


def main():
    pdf = test_data_path('manual.pdf')
    pages = Pdfconduit(pdf).info.pages

    last_time = None
    first_time = None

    print('PDF Conduit - Flatten execution time based on number of pages')
    print('-' * 49)
    print('{0:6} | {1:12} | {2:9} | {3:9}'.format('Pages', 'Time', '+1 increase', '+x increase'))
    print('-' * 49)

    for num_pages in range(1, max(pages + 1, 50)):
        sliced = Pdfconduit(pdf).set_output_temp().slice(1, num_pages)

        t = Timer()
        flattened = sliced.flatten()
        end = round((time() - t.start) * 1000, 2)

        if not first_time:
            first_time = end

        increase1 = round((float(end) / float(last_time) - 1) * 100, 1) if last_time else 0
        increase2 = round((float(end) / float(first_time) - 1) * 100, 1) if first_time else 0
        print('{0:6} | {1:8} mms | {2:10}% | {3:10}%'.format(num_pages, end, increase1, increase2))
        last_time = end


if __name__ == '__main__':
    main()