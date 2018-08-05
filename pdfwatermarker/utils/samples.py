# Generate sample PDF documents
import os
from pdfwatermarker import Watermark, open_window, merge, slicer, info
from pdfwatermarker.watermark.draw import available_images, CanvasObjects, CanvasStr, WatermarkDraw
from pdfwatermarker.watermark.lib.gui import get_directory, get_file
from tqdm import tqdm


def watermarks(destination, images=available_images()):
    watermarks = []
    w = Watermark(destination, use_receipt=False, open_file=False, remove_temps=True)
    for i in images:
        wm = w.draw(text1=i,
                    image=i,
                    copyright=False)
        watermarks.append(wm)
    m = merge(watermarks, 'Watermarks samples', destination)
    return w, m


def opacity(source):
    _source = source
    samples = []
    _range = range(4, 25)[::3]
    wm = Watermark(source, use_receipt=False, open_file=False, remove_temps=False)
    if info.pages_count(source) > 2:
        source = slicer(source, 1, 1, wm.tempdir)
    for i in tqdm(_range):
        o = i * .01
        wtrmrk = wm.draw(text1='200 Stonewall Blvd', text2='Wrentham, MA', opacity=o)
        watermarked = wm.add(document=source, watermark=wtrmrk, output='temp')

        objects = CanvasObjects()
        objects.add(CanvasStr(str(str(i).zfill(2) + '%'), opacity=1, x=15, y=30, x_centered=False))
        label = WatermarkDraw(objects, tempdir=wm.tempdir).write()

        wtrmrk_with_label = wm.add(watermarked, label, output='temp')
        samples.append(wtrmrk_with_label)
    m = merge(samples, 'Opacity comparison samples', os.path.dirname(_source))
    return wm, m


def placement(source):
    _source = source
    wm = Watermark(source, use_receipt=False, open_file=False, remove_temps=True)
    if info.pages_count(source) > 2:
        source = slicer(source, 1, 1, wm.tempdir)
    wtrmrk = wm.draw(text1='200 Stonewall Blvd',
                     text2='Wrentham, MA')
    over = wm.add(document=source, watermark=wtrmrk, output='temp', underneath=False)
    objects = CanvasObjects()
    objects.add(CanvasStr('Overlayed', size=14, opacity=1, x=15, y=30, x_centered=False))
    label = WatermarkDraw(objects, tempdir=wm.tempdir).write()
    over_with_label = wm.add(over, label, output='temp')

    under = wm.add(document=source, watermark=wtrmrk, output='temp', underneath=True)
    objects = CanvasObjects()
    objects.add(CanvasStr('Underneath', size=14, opacity=1, x=15, y=30, x_centered=False))
    label = WatermarkDraw(objects, tempdir=wm.tempdir).write()
    under_with_label = wm.add(under, label, output='temp')
    m = merge([over_with_label, under_with_label], 'Watermark Placement samples', os.path.dirname(_source))
    return wm, m


def main():
    src = get_file()
    dst = os.path.dirname(src)
    wm, m = watermarks(dst)
    wm, m = opacity(src)
    wm, m = placement(src)

    wm.cleanup(receipt=False)
    open_window(m)


if __name__ == '__main__':
    main()
