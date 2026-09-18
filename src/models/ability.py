from dataclasses import dataclass

@dataclass
class Ability:
    name: str
    ability_type: str  # "once_per_turn", "infinite", "passive"
    effect: Effect  # What the ability does
    description: Optional[str] = ""
    req_active: bool = False #does the pokemon have to be in active position for the ability to become usable