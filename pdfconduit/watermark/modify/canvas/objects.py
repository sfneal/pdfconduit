from typing import Optional

from pdfconduit.watermark.modify import LETTER


class CanvasStr:
    """Canvas string data object used for storing canvas.drawString parameters."""

    def __init__(
        self,
        string: str,
        font: str = "Vera",
        color: str = "black",
        size: int = 40,
        opacity: float = 0.1,
        x: float = 0,
        y: float = 0,
        x_centered: bool = True,
        y_centered: bool = False,
    ):
        self.string = string
        self.font = font
        self.color = color
        self.size = size
        self.opacity = opacity
        self.x = x
        self.y = y
        self.x_centered = x_centered
        self.y_centered = y_centered


class CanvasImg:
    """Canvas image data object used for storing canvas.drawImage parameters."""

    def __init__(
        self,
        image: str,
        opacity: float = 0.1,
        x: float = 0,
        y: float = 0,
        w: int = LETTER[0],
        h: int = LETTER[1],
        mask: Optional[str] = "auto",
        preserve_aspect_ratio: bool = True,
        centered: bool = False,
    ):
        self.image = image
        self.opacity = opacity
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.mask = mask
        self.preserve_aspect_ratio = preserve_aspect_ratio
        self.centered = centered


class CanvasObjects:
    """Canvas object collector to store list of canvas objects."""

    def __init__(self):
        self.objects = []

    def __iter__(self) -> iter:
        return iter(self.objects)

    def add(self, canvas_object) -> None:
        self.objects.append(canvas_object)
