from pdfwatermarker.watermark.canvas import pil_create_letter, pil_draw_text_centered, pil_save
from tests import directory, pdf


def main():
    img = pil_create_letter()
    img = pil_draw_text_centered(img, 'Hello World')
    i = pil_save(img, directory)
    print(i)


if __name__ == '__main__':
    main()
