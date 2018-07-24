from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.styles import getSampleStyleSheet


styles = getSampleStyleSheet()


def encrypt(pdf, password):
    pdf_writer = PdfFileWriter()

    with open(pdf, 'rb') as pdf_file:
        print('PDF file opened')
        pdf_reader = PdfFileReader(pdf_file)
        print('PDF file read')

        print('PDF writer object created')
        for page_num in range(pdf_reader.numPages):
            pdf_writer.addPage(pdf_reader.getPage(page_num))
        print('PDF file pages added to writer object')

        # PDF out never finishes writing when code below is uncommented
        pdf_writer.encrypt(password)
        print('PDF writer encrypted')

        with open('/Users/Stephen/Desktop/output.pdf', 'wb') as output_pdf:
            print('PDF output opened')
            pdf_writer.write(output_pdf)
            print('PDF output written')
        print('PDF output closed')


def main():
    pdf = '/Users/Stephen/Desktop/20110069_FP.1.pdf'
    # pdf = '/Users/Stephen/Desktop/test.pdf'
    password = 'test'
    encrypt(pdf, password)


if __name__ == '__main__':
    main()
