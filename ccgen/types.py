from dataclasses import dataclass, field
from typing import Dict, NewType, Optional, Set

Attribute = NewType('Attribute', str)
Attributes = NewType('Attributes', Set[Attribute])


@dataclass
class Enum:
    name: str
    items: Dict[str, int] = field(default_factory=dict)

    is_bits: bool = False
    is_stringable: bool = False
