from dataclasses import dataclass
from typing import Optional

@dataclass
class Effect:
    """Base class for all card effects."""
    type: str
    amount: Optional[int] = None
    target: Optional[str] = None
    target_condition: Optional[str] = None
    target_condition_instance: Optional[str] = None