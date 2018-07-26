# Add dynamic text to a watermark PDF template file
import io
import os
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pdfwatermarker import set_destination, resource_path, write_pdf
import sys


def bundle_dir():
    if getattr(sys, 'frozen', False):
        # we are running in a bundle
        bundle_dir = sys._MEIPASS
    else:
        # we are running in a normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
    return bundle_dir


def register_font():
    folder = bundle_dir + os.sep + 'lib'
    ttfFile = resource_path(os.path.join(folder, 'Vera.ttf'))
    pdfmetrics.registerFont(TTFont("Vera", ttfFile))


bundle_dir = bundle_dir()
register_font()
default_template = resource_path(bundle_dir + os.sep + 'lib' + os.sep + 'watermark.pdf')


def center_str(txt, font, size, offset=120):
    page_width = letter[1]
    text_width = stringWidth(txt, fontName=font, fontSize=size)
    return ((page_width - text_width) / 2.0) + offset


class WatermarkDraw:
    def __init__(self, project, text, pdf, template=default_template, font='Vera', opacity=0.1):
        self.text = text
        self.template = template
        self.font = font
        self.opacity = opacity

        # create a new PDF with Reportlab
        self.packet = io.BytesIO()
        self.can = Canvas(self.packet, pagesize=letter)  # Initialize canvas
        self.dst = resource_path(set_destination(pdf, project, 'watermark'))
        self.draw()

        self.packet.seek(0)  # move to the beginning of the StringIO buffer
        write_pdf(self.packet, self.template, self.dst)  # Save new pdf file

    def __str__(self):
        return str(self.dst)

    def _draw_address(self):
        # Address
        self.can.setFont(self.font, self.text['address']['font'])  # Large font for address
        self.can.setFillColor('black', self.opacity)
        self.can.rotate(30)
        address = self.text['address']['txt']['address']
        self.can.drawString(x=center_str(address, self.font, self.text['address']['font']),
                            y=self.text['address']['y'],
                            text=address)

    def _draw_town_state(self):
        # Town and State
        town_state = self.text['address']['txt']['town'] + ', ' + self.text['address']['txt']['state']
        self.can.drawString(x=center_str(town_state, self.font, self.text['address']['font']),
                            y=self.text['address']['y'] + 50,
                            text=town_state)

    def _draw_copyright(self):
        # Copyright
        self.can.setFont(self.font, self.text['copyright']['font'])  # Smaller font for copyright
        cright = self.text['copyright']['txt']
        self.can.drawString(x=center_str(cright, self.font, self.text['copyright']['font']),
                            y=self.text['copyright']['y'],
                            text=cright)

    def draw(self):
        # Draw watermark elements
        self._draw_address()
        self._draw_town_state()
        self._draw_copyright()
        self.can.save()  # Save canvas
