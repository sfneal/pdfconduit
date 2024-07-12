# Encrypt a PDF file with password protection
from enum import Enum
from typing import Optional

from pypdf import PdfWriter
from pypdf.constants import UserAccessPermissions

from pdfconduit.utils import add_suffix
from pdfconduit.utils.read import pypdf_reader


class Algorithms(Enum):
    RC4_40: str = 'RC4-40'
    RC4_128: str = 'RC4-128'
    AES_128: str = 'AES-128'
    AES_256_r5: str = 'AES-256-R5'
    AES_256: str = 'AES_256'


class Encrypt:
    def __init__(
        self,
        pdf: str,
        user_pw: str,
        owner_pw: Optional[str] = None,
        output: Optional[str] = None,
        suffix: str = "secured",
        bit128: bool = True,
        allow_printing: bool = True,
        allow_commenting: bool = False,
        overwrite_permission: Optional[int] = None,
        decrypt: Optional[str] = None,
        algorithm: Optional[Algorithms] = None
    ) -> None:
        """Password protect PDF file and allow all other permissions."""
        self.pdf = pdf
        self.user_pw = user_pw
        self.owner_pw = owner_pw
        self.output = add_suffix(pdf, suffix=suffix) if not output else output
        self.encrypt_128 = bit128
        self.allow_printing = allow_printing
        self.allow_commenting = allow_commenting
        self.overwrite_permission = overwrite_permission
        self.decrypt = decrypt

        if algorithm is not None:
            self.algorithm = algorithm
        elif not self.encrypt_128:
            self.algorithm = Algorithms.RC4_40
        else:
            self.algorithm = Algorithms.AES_128

        if self.algorithm == Algorithms.RC4_40:
            self.encrypt_128 = False

    def __str__(self) -> str:
        return str(self.output)

    def encrypt(self, decrypt: Optional[str] = None) -> str:
        decrypt = decrypt if decrypt else self.decrypt

        if self.allow_printing and self.allow_commenting:
            permissions = UserAccessPermissions.PRINT | UserAccessPermissions.MODIFY
        elif self.allow_printing:
            permissions = UserAccessPermissions.PRINT
        elif self.allow_commenting:
            permissions = UserAccessPermissions.MODIFY
        else:
            permissions = UserAccessPermissions

        with open(self.pdf, "rb") as pdf_file:
            # Read opened PDF file
            pdf_reader = pypdf_reader(pdf_file, decrypt)

            # Create PDF writer object
            pdf_writer = PdfWriter(clone_from=pdf_reader)

            # Apply encryption to writer object
            pdf_writer.encrypt(
                user_password=self.user_pw,
                owner_password=self.owner_pw,
                use_128bit=self.encrypt_128,
                permissions_flag=permissions,
                algorithm=self.algorithm.value
            )

            # todo: add metadata adding functionality
            pdf_writer.add_metadata(
                {
                    "/Producer": "pdfconduit",
                    "/Creator": "pdfconduit",
                    "/Author": "Stephen Neal",
                }
            )

            # Write encrypted PDF to file
            with open(self.output, "wb") as output_pdf:
                pdf_writer.write(output_pdf)
        return self.output


def main():
    from argparse import ArgumentParser

    # TODO: Finish implementing argparse

    # Declare argparse argument descriptions
    usage = "Encrypt PDF files"
    description = "Password protect a PDF file by applying encryption."
    helpers = {
        "pdf": "PDF file to encrypt",
        "p": "Retrieve Python interpreter information such as Python version and Python compiler",
        "s": "Retrieve software related information such as operating system, machine type, username, etc.",
        "hw": "Retrieve Hardware related information such as memory and processor information",
    }

    # construct the argument parse and parse the arguments
    ap = ArgumentParser(usage=usage, description=description)
    ap.add_argument("pdf", help=helpers["pdf"])
    ap.add_argument("-upw", "--user_pw", help=helpers["upw"])
    ap.add_argument("-opw", "--owner_pw", help=helpers["opw"])
    ap.add_argument("-out", "--output", help=helpers["out"])
    args = vars(ap.parse_args())


if __name__ == "__main__":
    main()
