from abc import ABC, abstractmethod
from enum import Enum

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class Driver(Enum):
    pdfrw: str = 'pdfrw'
    pypdf: str = 'pypdf'


class PdfDriver(ABC):
    _driver: Driver = Driver.pdfrw

    def use_pdfrw(self) -> Self:
        self._driver = Driver.pdfrw
        return self

    def use_pypdf(self) -> Self:
        self._driver = Driver.pypdf
        return self

    def is_driver_pdfrw(self) -> bool:
        return self._driver == Driver.pdfrw

    def is_driver_pypdf(self) -> bool:
        return self._driver == Driver.pypdf

    @abstractmethod
    def pdfrw(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def pypdf(self) -> str:
        raise NotImplementedError
