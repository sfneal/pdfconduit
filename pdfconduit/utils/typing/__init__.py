from dataclasses import dataclass
from io import BytesIO
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

try:
    from typing import Annotated, Self, TypedDict
except ImportError:
    from typing_extensions import Annotated, Self, TypedDict


PdfObject = Union[str, BytesIO]
PdfObjects = Iterable[PdfObject]


@dataclass
class _ImageQualityRange:
    min: int = 1
    max: int = 99


ImageQuality = Annotated[int, _ImageQualityRange]

ScaleMargins = Tuple[int, int]


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
    ImageQuality,
    ScaleMargins,
]
