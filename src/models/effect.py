from dataclasses import dataclass
from typing import Optional

@dataclass
class Effect:
    """Base class for all card effects."""
    effect_type: str
    amount: Optional[int] = None
    target: Optional[str] = None
    target_location: Optional[str] = None
    target_condition: Optional[str] = None