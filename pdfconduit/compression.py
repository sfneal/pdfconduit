from dataclasses import dataclass
from enum import Enum

from pdfconduit.utils.typing import List, Self


class Compression(Enum):
    DEFAULT: int = -1
    NONE: int = 0
    BEST_SPEED: int = 1
    BEST_COMPRESSION: int = 9
    LEVEL_0: int = 0
    LEVEL_1: int = 1
    LEVEL_2: int = 2
    LEVEL_3: int = 3
    LEVEL_4: int = 4
    LEVEL_5: int = 5
    LEVEL_6: int = 6
    LEVEL_7: int = 7
    LEVEL_8: int = 8
    LEVEL_9: int = 9

    @classmethod
    def from_level(cls, level):
        return cls(level)

    @classmethod
    def all(cls) -> List[Self]:
        return list(map(lambda c: c, cls))


@dataclass
class ImageQualityRange:
    min: int = 1
    max: int = 99
