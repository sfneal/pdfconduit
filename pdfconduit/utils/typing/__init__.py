from io import BytesIO
from typing import Optional, Any, Tuple, Dict, Union, List, Iterable

try:
    from typing import Self, Annotated, TypedDict
except ImportError:
    from typing_extensions import Self, Annotated, TypedDict

PdfObject = Union[str, BytesIO]
PdfObjects = Iterable[PdfObject]


__all__ = [
    Optional,
    Any,
    Tuple,
    Dict,
    Self,
    Annotated,
    TypedDict,
    Union,
    List,
    Iterable,
    PdfObject,
    PdfObjects,
]
