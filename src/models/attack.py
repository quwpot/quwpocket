from dataclasses import dataclass
from typing import Optional

@dataclass
class AttackRequirement:
    energy_type: str  #water, fire, ...
    amount: int

@dataclass
class Attack:
    name: str
    damage: int
    cost: list[AttackRequirement]
    effect: Optional[str] = None #side effects like discarding energy
    description: str = ""