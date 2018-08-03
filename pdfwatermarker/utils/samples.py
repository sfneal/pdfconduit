# Generate sample PDF documents
import os
from pdfwatermarker import Watermark, open_window, merge
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
    return wm, m


def opacity(source):
    samples = []
    _range = range(4, 25)[::3]
    wm = Watermark(source, use_receipt=False, open_file=False, remove_temps=False)
    for i in tqdm(_range):
        o = i * .01
        wtrmrk = wm.draw(text1='200 Stonewall Blvd', text2='Wrentham, MA', opacity=o)
        watermarked = wm.add(document=source, watermark=wtrmrk, output='temp')

        objects = CanvasObjects()
        objects.add(CanvasStr(str(str(i).zfill(2) + '%'), opacity=1, x=15, y=30, x_centered=False))
        label = WatermarkDraw(objects, tempdir=wm.tempdir).write()

        wtrmrk_with_label = wm.add(watermarked, label, output='temp')
        samples.append(wtrmrk_with_label)
    m = merge(samples, 'Opacity comparison samples', os.path.dirname(source))
    return wm, m


def placement(source):
    wm = Watermark(source, use_receipt=False, open_file=False, remove_temps=True)
    wtrmrk = wm.draw(text1='200 Stonewall Blvd',
                     text2='Wrentham, MA')
    over = wm.add(document=source, watermark=wtrmrk, output='temp', underneath=False)
    under = wm.add(document=source, watermark=wtrmrk, output='temp', underneath=True)
    m = merge([over, under], 'Watermark Placement samples', os.path.dirname(source))
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
