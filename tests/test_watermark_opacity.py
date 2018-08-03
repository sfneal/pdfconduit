# Test opacity outputs
from pdfwatermarker import Watermark, merge
from pdfwatermarker.watermark.draw import WatermarkDraw
import os
import shutil
from tqdm import tqdm


def main():
    print('Testing Watermark class reliability')
    directory = '/Users/Stephen/Desktop/'

    pdf = os.path.join(directory, '20150065_FP.1.pdf')
    project = '20160054'
    address = '43 Indian Lane'
    town = 'Franklin'
    state = 'MA'

    if os.path.isdir(os.path.join(directory, 'opacity')):
        shutil.rmtree(os.path.join(directory, 'opacity'))
    os.mkdir(os.path.join(directory, 'opacity'))

    _range = range(4, 25)[::3]
    for i in tqdm(_range):
        o = i * .01
        wm = str(Watermark(pdf, project, address, town, state, opacity=o, remove_temps=True, open_file=False))
        new_name = os.path.join(directory, 'opacity', str(str(i).zfill(2) + '%') + '.pdf')
        os.rename(wm, new_name)
        TextDraw(new_name, str(str(i) + '%'), output_overwrite=True, font_size=24)
    wm = str(Watermark(pdf, project, address, town, state, opacity=1, remove_temps=False, open_file=True))

    opac_dir = os.path.join(directory, 'opacity')
    pdf_samples = sorted([os.path.join(opac_dir, i) for i in os.listdir(opac_dir)
                          if os.path.isfile(os.path.join(opac_dir, i))])
    merge(pdf_samples, 'opacity samples')


if __name__ == '__main__':
    main()
