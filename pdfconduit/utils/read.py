from PyPDF3 import PdfFileReader
from pypdf import PdfReader


def pypdf3_reader(pdf, decrypt=None) -> PdfFileReader:
    """
    Retrieve a PdfFileReader object that has been decrypted if a password is specified.

    :param pdf: PDF document to read
    :param decrypt: Owner password to decrypt pdf
    :return: PdfFileReader object
    """
    if decrypt:
        reader = PdfFileReader(pdf)
        reader.decrypt(decrypt)
        return reader
    else:
        return PdfFileReader(pdf)


def pypdf_reader(pdf, decrypt=None) -> PdfReader:
    """
    Retrieve a PdfFileReader object that has been decrypted if a password is specified.

    :param pdf: PDF document to read
    :param decrypt: Owner password to decrypt pdf
    :return: PdfFileReader object
    """
    if decrypt:
        reader = PdfReader(pdf)
        reader.decrypt(decrypt)
        return reader
    else:
        return PdfReader(pdf)
