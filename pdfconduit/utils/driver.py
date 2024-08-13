from abc import ABC, abstractmethod
from enum import Enum

from pdfconduit.utils.typing import Self


class Driver(Enum):
    pdfrw: str = "pdfrw"
    pypdf: str = "pypdf"


class PdfDriver(ABC):
    _driver: Driver = Driver.pdfrw

    def use_pdfrw(self) -> Self:
        return self.use(Driver.pdfrw)

    def use_pypdf(self) -> Self:
        return self.use(Driver.pypdf)

    def use(self, driver: Driver) -> Self:
        self._driver = driver
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

    def execute(self) -> str:
        return self.pdfrw() if self.is_driver_pdfrw() else self.pypdf()
