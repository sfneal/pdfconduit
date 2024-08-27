from typing import Optional, List, Dict, Tuple, TypedDict

from pypdf import DocumentInformation, PageObject


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
    dimensions: DimensionsDict
    size: SizeTuple
    rotate: int
    permissions: Dict[str, bool]
    images_count: int



__all__ = ['SecurityDict', 'DimensionsDict', 'SizeTuple', 'Metadata', 'Resources', 'InfoAllDict']