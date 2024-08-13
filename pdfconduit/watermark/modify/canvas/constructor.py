from datetime import datetime
from typing import Optional, Union, Tuple

from PillowImage import PillowImage

from pdfconduit.watermark.modify.canvas.objects import (
    CanvasObjects,
    CanvasStr,
    CanvasImg,
)


class CanvasConstructor:
    def __init__(
        self,
        text1: str = None,
        text2: str = None,
        copyright_: Optional[bool] = None,
        image: Optional[str] = None,
        rotate: int = 0,
        opacity: Union[int, float] = 8,
        tempdir: Optional[str] = None,
    ):
        self.text1 = text1
        self.text2 = text2
        self.copyright = copyright_
        self.image = image
        self.rotate = rotate
        self.opacity = opacity
        self.tempdir = tempdir

        # Initialize CanvasObjects collector class and add objects
        self.obj = CanvasObjects()

    @property
    def objects(self) -> Tuple[CanvasObjects, int]:
        return self.obj, self.rotate

    def canvas(self) -> Tuple[CanvasObjects, int]:
        if self.image is not None:
            self.obj.add(CanvasImg(self.image, opacity=self.opacity, x=0, y=253))

            if self.text1 and self.text2 and self.copyright:
                self.obj.add(
                    CanvasStr(
                        "© copyright " + str(datetime.now().year),
                        size=16,
                        y=-170,
                        opacity=self.opacity,
                    )
                )
                self.obj.add(
                    CanvasStr(self.text1, opacity=self.opacity, size=40, y=-360)
                )
                self.obj.add(
                    CanvasStr(self.text2, opacity=self.opacity, size=40, y=-560)
                )
            elif self.text1 and self.text2 and not self.copyright:
                self.obj.add(CanvasStr(self.text1, opacity=self.opacity, size=40, y=90))
                self.obj.add(CanvasStr(self.text2, opacity=self.opacity, size=40, y=0))
            elif self.text1:
                self.obj.add(
                    CanvasStr(self.text1, opacity=self.opacity, size=40, y=-125)
                )
            elif self.copyright:
                self.obj.add(
                    CanvasStr(self.text1, opacity=self.opacity, size=40, y=-125)
                )

        else:
            if self.text1 and self.text2 and self.copyright:
                self.obj.add(
                    CanvasStr(self.text1, opacity=self.opacity, size=80, y=110)
                )
                self.obj.add(CanvasStr(self.text2, opacity=self.opacity, size=80, y=20))
                self.obj.add(
                    CanvasStr(
                        "© copyright " + str(datetime.now().year),
                        size=16,
                        y=-30,
                        opacity=self.opacity,
                    )
                )
            elif self.text1 and self.text2 and not self.copyright:
                self.obj.add(CanvasStr(self.text1, opacity=self.opacity, size=80, y=90))
                self.obj.add(CanvasStr(self.text2, opacity=self.opacity, size=80, y=0))
            elif self.text1:
                self.obj.add(
                    CanvasStr(self.text1, opacity=self.opacity, size=40, y=-125)
                )
            elif self.copyright:
                self.obj.add(
                    CanvasStr(
                        "© copyright " + str(datetime.now().year),
                        opacity=self.opacity,
                        size=16,
                        y=50,
                    )
                )
        return self.objects

    def img(self) -> Tuple[CanvasObjects, int]:
        with PillowImage() as img:
            if self.image is not None:
                img.draw_img(self.image, x=0, y=50, opacity=self.opacity)

                if self.text1 and self.text2 and self.copyright:
                    img.draw_text(self.text1, font_size=40, y=416, opacity=self.opacity)
                    img.draw_text(self.text2, font_size=40, y=466, opacity=self.opacity)
                    img.draw_text(
                        "© copyright " + str(datetime.now().year),
                        font_size=16,
                        y="center",
                    )
                elif self.text1 and self.text2 and not self.copyright:
                    img.draw_text(self.text1, font_size=40, y=416, opacity=self.opacity)
                    img.draw_text(self.text2, font_size=40, y=466, opacity=self.opacity)
                elif self.text1:
                    self.obj.add(
                        CanvasStr(self.text1, opacity=self.opacity, size=40, y=-125)
                    )
                elif self.copyright:
                    img.draw_text(
                        "© copyright " + str(datetime.now().year),
                        font_size=16,
                        y="center",
                    )
            else:
                if self.text1 and self.text2 and self.copyright:
                    img.draw_text(
                        "© copyright " + str(datetime.now().year), font_size=16, y=350
                    )
                    img.draw_text(self.text1, font_size=80, y=106, opacity=self.opacity)
                    img.draw_text(self.text2, font_size=80, y=206, opacity=self.opacity)
                elif self.text1 and self.text2 and not self.copyright:
                    img.draw_text(self.text1, font_size=80, y=106, opacity=self.opacity)
                    img.draw_text(self.text2, font_size=80, y=206, opacity=self.opacity)
                elif self.text1:
                    img.draw_text(self.text1, font_size=80, y=106, opacity=self.opacity)
                elif self.copyright:
                    img.draw_text(
                        "© copyright " + str(datetime.now().year), font_size=16, y=350
                    )

            img.rotate(self.rotate)
            self.rotate = 0
            i = img.save(destination=self.tempdir)
            self.obj.add(CanvasImg(i, opacity=1, centered=True))
            return self.objects
