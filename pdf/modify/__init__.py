from reportlab.lib.pagesizes import letter
from pdf.modify.draw.image import DrawPIL


LETTER = letter[1], letter[0]


__all__ = ['LETTER', 'DrawPIL']
