# Encrypt a PDF file with password protection
import os
from pdfwatermarker.utils import add_suffix
from pdfwatermarker.thirdparty.PyPDF2 import PdfFileReader
from pdfwatermarker.utils.override import PdfFileWriter2


class EncryptParams:
    def __init__(self, user_pw, owner_pw=None, allow_printing=True, output=None):
        self.user_pw = user_pw
        self.owner_pw = owner_pw
        self.allow_printing = allow_printing
        self.output = output

    def __str__(self):
        return str(self.__dict__)


def encrypt(pdf, user_pw, owner_pw=None, output=None, encrypt_128=True, restrict_permission=True):
    """
    Password protect PDF file and allow all other permissions.
    Utilizes PyPDF2 reader and writer classes.
    """
    # Create output filename if not already set
    if not output:
        output = add_suffix(pdf, 'secured')

    # Create PDF writer object
    pdf_writer = PdfFileWriter2()
    with open(pdf, 'rb') as pdf_file:
        # Read opened PDF file
        pdf_reader = PdfFileReader(pdf_file)

        # Add each page from source PDF
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            pdf_writer.addPage(page)

        # Apply encryption to writer object
        pdf_writer.encrypt(user_pw, owner_pw, use_128bit=encrypt_128, restrict_permission=restrict_permission)

        pdf_writer.addMetadata({
            '/Producer': 'pdfwatermarker',
            '/Creator': 'HPA Design',
            '/Author': 'HPA Design',
        })

        # Write encrypted PDF to file
        with open(output, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)
        return output


PDFTK_PATH = '/opt/pdflabs/pdftk/bin/pdftk'


def get_pdftk_path():
    if os.path.exists(PDFTK_PATH):
        return PDFTK_PATH


def secure(pdf, user_pw, owner_pw, restrict_permission=True, pdftk=get_pdftk_path(), output=None):
    """
    Encrypt a PDF file and restrict permissions to print only.
    Utilizes pdftk command line tool.
    """
    if pdftk:
        # Check that PDF file is encrypted
        with open(pdf, 'rb') as f:
            reader = PdfFileReader(f)
            if reader.isEncrypted:
                print('PDF is already encrypted')
                return pdf

        # Create output filename if not already set
        if not output:
            output = add_suffix(pdf, 'secured')

        # Replace spaces within paths with backslashes followed by a space
        pdf_en = pdf.replace(' ', '\ ')
        output_en = output.replace(' ', '\ ')

        # Concatenate bash command
        command = pdftk + ' ' + pdf_en + ' output ' + output_en + ' owner_pw ' + owner_pw + ' user_pw ' + user_pw

        # Append string to command if printing is allowed
        if restrict_permission:
            command += ' allow printing'

        # Execute command
        os.system(command)
        return output
