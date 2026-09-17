from dataclasses import dataclass
from typing import Optional
from src.models.effect import Effect

@dataclass
class AttackRequirement:
    energy_type: str  #water, fire, ...
    amount: int

@dataclass
class Attack:
    name: str
    damage: int
    cost: list[AttackRequirement]
    effect: Optional[Effect] = None #side effects like discarding energy
    description: str = ""
    needs_target: bool = False