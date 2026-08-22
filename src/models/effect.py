from dataclasses import dataclass
from typing import Optional

@dataclass
class Effect:
    """Base class for all card effects."""
    effect_type: str
    amount: Optional[int] = None
    instance: Optional[str] = None #e.g specifying which type of energy to attach
    target: Optional[str] = None
    target_condition: Optional[str] = None
    target_condition_instance: Optional[str] = None
    target_condition_2: Optional[str] = None
    target_condition_instance_2: Optional[str] = None