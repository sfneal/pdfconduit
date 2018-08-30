from datetime import datetime
from .objects import CanvasObjects, CanvasStr, CanvasImg
from ..draw.image import DrawPIL


class CanvasConstructor:
    def __init__(self, text1=None, text2=None, copyright=None, image=None, rotate=0, opacity=0.08, tempdir=None):
        self.text1 = text1
        self.text2 = text2
        self.copyright = copyright
        self.image = image
        self.rotate = rotate
        self.opacity = opacity
        self.tempdir = tempdir

        # Initialize CanvasObjects collector class and add objects
        self.obj = CanvasObjects()

    @property
    def objects(self):
        return self.obj, self.rotate

    def canvas(self):
        if self.image is not None:
            self.obj.add(CanvasImg(self.image, opacity=self.opacity, x=0, y=253))

            if self.text2 and self.copyright:
                self.obj.add(CanvasStr('© copyright ' + str(datetime.now().year), size=16, y=-170,
                                       opacity=self.opacity))
                self.obj.add(CanvasStr(self.text1, opacity=self.opacity, size=40, y=-360))
                self.obj.add(CanvasStr(self.text2, opacity=self.opacity, size=40, y=-560))
            elif self.text2 and not self.copyright:
                self.obj.add(CanvasStr(self.text1, opacity=self.opacity, size=40, y=90))
                self.obj.add(CanvasStr(self.text2, opacity=self.opacity, size=40, y=0))
            else:
                self.obj.add(CanvasStr(self.text1, opacity=self.opacity, size=40, y=-125))
        else:
            if self.text2 and self.copyright:
                self.obj.add(CanvasStr(self.text1, opacity=self.opacity, size=80, y=110))
                self.obj.add(CanvasStr(self.text2, opacity=self.opacity, size=80, y=20))
                self.obj.add(CanvasStr('© copyright ' + str(datetime.now().year), size=16, y=-30, opacity=self.opacity))
            elif self.text2 and not self.copyright:
                self.obj.add(CanvasStr(self.text1, opacity=self.opacity, size=80, y=90))
                self.obj.add(CanvasStr(self.text2, opacity=self.opacity, size=80, y=0))
            else:
                self.obj.add(CanvasStr(self.text1, opacity=self.opacity, size=40, y=50))
        return self.objects

    def img(self):
        img = DrawPIL(tempdir=self.tempdir)

        if self.image is not None:
            img.draw_img(self.image, x=0, y=50, opacity=self.opacity)
            if self.copyright:
                img.draw_text('© copyright ' + str(datetime.now().year), size=16, y='center')
            if self.text2:
                img.draw_text(self.text1, size=40, y=416, opacity=self.opacity)
                img.draw_text(self.text2, size=40, y=466, opacity=self.opacity)
            else:
                img.draw_text(self.text2, size=40, y=427, opacity=self.opacity)
        else:
            if self.text2 and self.copyright:
                img.draw_text('© copyright ' + str(datetime.now().year), size=16, y=350)
                img.draw_text(self.text1, size=80, y=106, opacity=self.opacity)
                img.draw_text(self.text2, size=80, y=206, opacity=self.opacity)
            elif self.text2 and not self.copyright:
                img.draw_text(self.text1, size=80, y=106, opacity=self.opacity)
                img.draw_text(self.text2, size=80, y=206, opacity=self.opacity)
            else:
                img.draw_text(self.text1, size=80, y='center', opacity=self.opacity)

        img.rotate(self.rotate)
        self.rotate = 0
        i = img.save()
        self.obj.add(CanvasImg(i, opacity=1, centered=True))
        return self.objects