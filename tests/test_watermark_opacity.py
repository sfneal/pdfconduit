from pdfwatermarker import Watermark
import os
import shutil
from tqdm import tqdm


def main():
    print('Testing Watermark class reliability')
    directory = '/Users/Stephen/Desktop/'

    pdf = os.path.join(directory, '20150094_Market Model.pdf')
    project = '20160054'
    address = '43 Indian Lane'
    town = 'Franklin'
    state = 'MA'

    if os.path.isdir(os.path.join(directory, 'opacity')):
        shutil.rmtree(os.path.join(directory, 'opacity'))
    os.mkdir(os.path.join(directory, 'opacity'))

    for i in tqdm(range(1, 21)):
        o = i * .01
        wm = str(Watermark(pdf, project, address, town, state, opacity=o, remove_temps=False, open_file=False))
        os.rename(wm, os.path.join(directory, 'opacity', str(o) + '.pdf'))


if __name__ == '__main__':
    main()
