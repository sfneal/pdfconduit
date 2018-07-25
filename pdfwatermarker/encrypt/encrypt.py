# Encrypt a PDF file with password protection
from pdfwatermarker import add_suffix
from PyPDF2 import PdfFileReader, PdfFileWriter
import os


def protect(pdf, user_pw, owner_pw=None):
    """Password protect PDF file and allow all other permissions"""
    pdf_writer = PdfFileWriter()
    with open(pdf, 'rb') as pdf_file:
        pdf_reader = PdfFileReader(pdf_file)

        for page_num in range(pdf_reader.numPages):
            pdf_writer.addPage(pdf_reader.getPage(page_num))

        pdf_writer.encrypt(user_pw, owner_pw)

        with open(add_suffix(pdf, 'protected'), 'wb') as output_pdf:
            pdf_writer.write(output_pdf)
        print('PDF Protecting Done!')


def secure(pdf, user_pw, owner_pw, allow_printing=True, pdftk='/usr/local/bin/pdftk'):
    """Execute pdftk command line operation to encrypt a PDF file and restrict permissions to print only"""
    out = add_suffix(pdf, 'secured')
    command = pdftk + ' ' + pdf + ' output ' + out + ' owner_pw ' + owner_pw + ' user_pw ' + user_pw
    if allow_printing:
        command += ' allow printing'
    os.system(command)
    print('PDF Securing Done!')
