from dataclasses import dataclass
from enum import Enum
from typing import Optional

from pypdf.constants import UserAccessPermissions


class Algorithms(Enum):
    RC4_40: str = "RC4-40"
    RC4_128: str = "RC4-128"
    AES_128: str = "AES-128"
    AES_256: str = "AES-256"
    AES_256_r5: str = "AES-256-R5"

    @property
    def bit_length(self):
        if "40" in self.value:
            return 40
        elif "128" in self.value:
            return 128
        elif "256" in self.value:
            return 256

    @property
    def is_40bit(self) -> bool:
        return self.bit_length == 40

    @property
    def is_128bit(self) -> bool:
        return self.bit_length == 128

    @property
    def is_256bit(self) -> bool:
        return self.bit_length == 256

    @classmethod
    def from_algo(cls, algo: str):
        return cls(algo)


@dataclass
class Encryption:
    user_pw: str
    owner_pw: Optional[str]
    allow_printing: bool = True
    allow_commenting: bool = False
    algo: Algorithms = Algorithms.AES_256_r5
    permissions: UserAccessPermissions = UserAccessPermissions

    def __post_init__(self):
        if self.allow_printing and self.allow_commenting:
            self.permissions = (
                UserAccessPermissions.PRINT | UserAccessPermissions.MODIFY
            )
        elif self.allow_printing:
            self.permissions = UserAccessPermissions.PRINT
        elif self.allow_commenting:
            self.permissions = UserAccessPermissions.MODIFY
        else:
            self.permissions = UserAccessPermissions.R2
