# Generate sample PDF documents
import os
from pdfwatermarker import Merge, slicer, info
from pdfwatermarker.utils import open_window
from pdfwatermarker.watermark.draw.canvas import available_images
from pdfwatermarker.watermark import Label, Watermark
from tests import pdf


def _title(title='PDF Samples'):
    return Label(pdf, title, title_page=True).watermark


def watermarks(destination, images=available_images()):
    watermarks = [_title('Watermark Images')]
    w = Watermark(destination, use_receipt=False, open_file=False, remove_temps=True)
    for i in images:
        wm = w.draw(text1=i,
                    image=i,
                    copyright=False)
        watermarks.append(wm)
    m = Merge(watermarks, 'Watermarks samples', destination)
    return m.file, w


def opacity(source, dst):
    samples = [_title('Opacity Comparisons')]
    _range = range(4, 25)[::3]
    wm = Watermark(source, use_receipt=False, open_file=False, remove_temps=True)
    if info.pages(source) > 2:
        source = slicer(source, 1, 1, wm.tempdir)
    for i in _range:
        o = i * .01
        wtrmrk = wm.draw(text1='200 Stonewall Blvd', text2='Wrentham, MA', opacity=o)
        watermarked = wm.add(document=source, watermark=wtrmrk, output='temp')

        labeled_pdf = Label(watermarked, str(str(i).zfill(2) + '%'), tempdir=wm.tempdir).write()
        samples.append(labeled_pdf)
    m = Merge(samples, 'Opacity comparison samples', dst)
    return m.file, wm


def placement(source, dst):
    wm = Watermark(source, use_receipt=False, open_file=False, remove_temps=True)
    if info.pages(source) > 2:
        source = slicer(source, 1, 1, wm.tempdir)
    wtrmrk = wm.draw(text1='200 Stonewall Blvd',
                     text2='Wrentham, MA')
    over = wm.add(document=source, watermark=wtrmrk, output='temp', underneath=False)
    over_with_label = Label(over, 'Overlayed watermark', tempdir=wm.tempdir).write()

    under = wm.add(document=source, watermark=wtrmrk, output='temp', underneath=True)
    under_with_label = Label(under, 'Underneath watermarked', tempdir=wm.tempdir).write()

    m = Merge([_title('Watermark Placement'), over_with_label, under_with_label], 'Watermark Placement samples', dst)
    return m.file, wm


def layering(source, dst):
    wm = Watermark(source, use_receipt=False, open_file=False, remove_temps=True)
    if info.pages(source) > 2:
        source = slicer(source, 1, 1, wm.tempdir)
    flat = wm.draw(text1='200 Stonewall Blvd', text2='Wrentham, MA', flatten=True)
    layered = wm.draw(text1='200 Stonewall Blvd', text2='Wrentham, MA', flatten=False)

    wtrmrked_flat = Label(wm.add(document=source, watermark=flat, output='temp'), 'Flat watermark',
                          tempdir=wm.tempdir).write()
    wtrmrked_layer = Label(wm.add(document=source, watermark=layered, output='temp'), 'Layered watermark',
                           tempdir=wm.tempdir).write()

    watermark_flat = Label(flat, 'Flat watermark', tempdir=wm.tempdir).write()
    watermark_layer = Label(layered, 'Layered watermark', tempdir=wm.tempdir).write()
    m = Merge([_title('Watermark Layering'), wtrmrked_flat, watermark_flat, wtrmrked_layer, watermark_layer],
              'Layering samples', dst)
    return m, wm


def main():
    src = pdf
    dst = os.path.join(os.path.dirname(src), 'samples')
    if not os.path.exists(dst):
        os.mkdir(dst)
    m, wm = watermarks(dst)
    m, wm = opacity(src, dst)
    m, wm = placement(src, dst)
    m, wm = layering(src, dst)

    wm.cleanup()
    open_window(m)


if __name__ == '__main__':
    main()
