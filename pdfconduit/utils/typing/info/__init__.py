from typing import Optional, List, Tuple, TypedDict

from pypdf import DocumentInformation, PageObject

from pdfconduit.utils._permissions import Permissions


class SecurityDict(TypedDict):
    key: str
    value: int


class DimensionsDict(TypedDict):
    w: float
    h: float

SizeTuple = Tuple[float, float]

Metadata = Optional[DocumentInformation]

Resources = List[PageObject]

class InfoAllDict(TypedDict):
    encrypted: bool
    pages: int
    metadata: Metadata
    security: SecurityDict
    size: SizeTuple
    rotate: int
    permissions: Optional[Permissions]
    images_count: int



__all__ = ['SecurityDict', 'DimensionsDict', 'SizeTuple', 'Metadata', 'Resources', 'InfoAllDict']