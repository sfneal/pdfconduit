from PyPDF3 import PdfFileReader


def pypdf3_reader(pdf, decrypt=None):
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
