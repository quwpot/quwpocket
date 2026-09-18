from dataclasses import dataclass, field

@dataclass
class Effect:
    effect_type: str
    target: str | None = None
    amount: int = 0
    instance: str | None = None
    # A list of condition dicts, ALL must pass (logical AND)
    target_conditions: list[dict] = field(default_factory=list)