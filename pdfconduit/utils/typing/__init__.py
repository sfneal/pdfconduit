from typing import Optional, Any, Tuple, Dict, Union

try:
    from typing import Self, Annotated
except ImportError:
    from typing_extensions import Self, Annotated


__all__ = [Optional, Any, Tuple, Dict, Self, Annotated]
