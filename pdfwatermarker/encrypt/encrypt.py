# Encrypt a PDF file with password protection
from pdfwatermarker import add_suffix
from PyPDF2 import PdfFileReader, PdfFileWriter
import os


def protect(pdf, user_pw, owner_pw=None, output=None):
    """
    Password protect PDF file and allow all other permissions.
    Utilizes PyPDF2 reader and writer classes.
    """
    # Create PDF writer object
    pdf_writer = PdfFileWriter()
    with open(pdf, 'rb') as pdf_file:
        # Read opened PDF file
        pdf_reader = PdfFileReader(pdf_file)

        # Write each page of PDF to writer object
        for page_num in range(pdf_reader.numPages):
            pdf_writer.addPage(pdf_reader.getPage(page_num))

        # Apply encryption to writer object
        pdf_writer.encrypt(user_pw, owner_pw)

        # Create output filename if not already set
        if not output:
            output = add_suffix(pdf, 'protected')

        # Write encrypted PDF to file
        with open(output, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)
        print('PDF Protecting Done!')


def secure(pdf, user_pw, owner_pw, allow_printing=True, pdftk='/usr/local/bin/pdftk', output=None):
    """
    Encrypt a PDF file and restrict permissions to print only.
    Utilizes pdftk command line tool.
    """
    # Create output filename if not already set
    if not output:
        output = add_suffix(pdf, 'secured')

    # Concatenate bash command
    command = pdftk + ' ' + pdf + ' output ' + output + ' owner_pw ' + owner_pw + ' user_pw ' + user_pw

    # Append string to command if printing is allowed
    if allow_printing:
        command += ' allow printing'

    # Execute command
    os.system(command)
    print('PDF Securing Done!')
