from pdfwatermarker.watermark.watermark import Watermark
from pdfwatermarker.watermark.draw import WatermarkDraw
from pdfwatermarker.utils.path import add_suffix
from pdfwatermarker.watermark.draw.image import CanvasObjects, CanvasStr


class Label(WatermarkDraw):
    def __init__(self, document, label, title_page=False, suffix=None, output=None, tempdir=None):
        super(Label, self).__init__(self._create_canvas_objects(label, title_page), tempdir=tempdir)
        self.document = document
        self.watermark = self._write()

        if suffix:
            suffix = label if not suffix else suffix
            self.output = add_suffix(self.document, suffix)
        elif output:
            self.output = output
        else:
            self.output = self.dst

    @staticmethod
    def _create_canvas_objects(label, title_page):
        objects = CanvasObjects()
        if not title_page:
            objects.add(CanvasStr(label, size=14, opacity=1, x=15, y=25, x_centered=False))
        else:
            objects.add(CanvasStr(label, size=60, opacity=1, y_centered=True))
        return objects

    def write(self, cleanup=False):
        wm = Watermark(self.document, tempdir=self.dir, use_receipt=False, open_file=False, remove_temps=True)
        labeled = wm.add(watermark=self.watermark, output=self.output)
        if cleanup:
            wm.cleanup()
        return labeled