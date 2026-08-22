@dataclass
class Ability:
    name: str
    description: str
    req_active: bool #does the pokemon have to be in active position for the ability to become usable
    ability_type: str  # "once_per_turn", "infinite", "passive"
    effect: Effect  # What the ability does
    used_this_turn: bool = False  # For once_per_turn abilities