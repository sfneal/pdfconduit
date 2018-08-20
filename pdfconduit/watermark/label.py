from pdfconduit.watermark.canvas import CanvasObjects, CanvasStr
from pdfconduit.watermark.watermark import Watermark
from pdfconduit.watermark.draw import WatermarkDraw
from pdfconduit.utils.info import Info
from pdfconduit.utils.path import add_suffix


class Label(WatermarkDraw):
    def __init__(self, document, label, title_page=False, suffix='labeled', output=None, tempdir=None):
        self.size = Info(document).size
        super(Label, self).__init__(self._create_canvas_objects(label, title_page),
                                    pagesize=self.size, tempdir=tempdir)
        self.document = document
        self.watermark = self._write()

        if output:
            self.output = output
        elif suffix:
            suffix = label if not suffix else suffix
            self.output = add_suffix(self.document, suffix)
        else:
            self.output = self.dst

    def _create_canvas_objects(self, label, title_page):
        objects = CanvasObjects()
        if not title_page:
            objects.add(CanvasStr(label, size=14, opacity=1,
                                  x=-(self.size[0] / 2) + 15,
                                  y=-(self.size[1] / 2) + 25, x_centered=False))
        else:
            objects.add(CanvasStr(label, size=60, opacity=1, y_centered=True))
        return objects

    def write(self, cleanup=True):
        wm = Watermark(self.document, tempdir=self.dir, use_receipt=False, open_file=False, remove_temps=True)
        labeled = wm.add(watermark=self.watermark, output=self.output)
        if cleanup:
            wm.cleanup()
        return labeled