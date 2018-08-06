from reportlab.lib.pagesizes import letter


class CanvasStr:
    """Canvas string data object used for storing canvas.drawString parameters."""
    def __init__(self, string, font='Vera', color='black', size=40, opacity=0.1, x=None, y=None,
                 x_centered=True):
        self.string = string
        self.font = font
        self.color = color
        self.size = size
        self.opacity = opacity
        self.x = x
        self.y = y
        self.x_centered = x_centered


class CanvasImg:
    """Canvas image data object used for storing canvas.drawImage parameters."""
    def __init__(self, image, opacity=0.1, x=0, y=0, w=letter[0], h=letter[1], mask='auto',
                 preserve_aspect_ratio=True):
        self.image = image
        self.opacity = opacity
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.mask = mask
        self.preserve_aspect_ratio = preserve_aspect_ratio


class CanvasObjects:
    """Canvas object collector to store list of canvas objects."""
    def __init__(self):
        self.objects = []

    def __iter__(self):
        return iter(self.objects)

    def add(self, canvas_object):
        self.objects.append(canvas_object)