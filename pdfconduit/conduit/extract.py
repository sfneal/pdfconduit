# Extract images from a PDF
from typing import Optional

from PIL import Image

from pdfconduit.utils.info import Info


# Todo: Fix img_extract and develop tests
def img_extract(pdf: str, password: Optional[str] = None) -> None:
    # Read PDF file
    reader = Info(pdf, password).pdf

    # Number of pages in input document
    page_count = reader.getNumPages()

    # 5c. Go through all the input file pages to add a watermark to them
    for page_number in range(page_count):
        # Merge the watermark with the page
        page = reader.getPage(page_number)

        xobj = page["/Resources"]["/XObject"].getObject()
        for obj in xobj:
            if xobj[obj]["/Subtype"] == "/Image":
                size = (xobj[obj]["/Width"], xobj[obj]["/Height"])
                data = xobj[obj].getData()
                if xobj[obj]["/ColorSpace"] == "/DeviceRGB":
                    mode = "RGB"
                else:
                    mode = "P"

                if xobj[obj]["/Filter"] == "/FlateDecode":
                    img = Image.frombytes(mode, size, data)
                    img.save(obj[1:] + ".png")  # TODO: Add save destination parameter
                elif xobj[obj]["/Filter"] == "/DCTDecode":
                    img = open(obj[1:] + ".jpg", "wb")
                    img.write(data)
                    img.close()
                elif xobj[obj]["/Filter"] == "/JPXDecode":
                    img = open(obj[1:] + ".jp2", "wb")
                    img.write(data)
                    img.close()


# TODO: Fix text extract and interpret extracted text
def text_extract(path, password=None):
    """Extract text from a PDF file"""
    pdf = Info(path, password).pdf

    return [pdf.getPage(i).extractText() for i in range(pdf.getNumPages())]
