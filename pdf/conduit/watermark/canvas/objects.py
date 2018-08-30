from pdf.utils import LETTER


class CanvasStr:
    """Canvas string data object used for storing canvas.drawString parameters."""
    def __init__(self, string, font='Vera', color='black', size=40, opacity=0.1, x=0, y=0,
                 x_centered=True, y_centered=False):
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
    def __init__(self, image, opacity=0.1, x=0, y=0, w=LETTER[0], h=LETTER[1], mask='auto',
                 preserve_aspect_ratio=True, centered=False):
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

    def __iter__(self):
        return iter(self.objects)

    def add(self, canvas_object):
        self.objects.append(canvas_object)
