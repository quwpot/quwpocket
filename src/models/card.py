from dataclasses import dataclass #dataclasses are classes for storing data (duh) and assist by automatically generating stuff like __init__ or __repr__

@dataclass
class Card:
    """Basic class for all Cards
name: the displayed name
card_type: either Pokemon or Trainer"""
    name: str
    card_type: str

@dataclass
class Pokemon(Card):
    """Class tracking all stats that makes a Pokemon unique.
hp: current health points. start at max, decrease when damaged.
damage: amount of hp enemy pokemon lose if they get attacked
ex pokemon give two points when KO'd.
attached_energy: amount of energy tokens (currency required to unleash attacks) are currently equipped. starts at 0 and increases as game progresses."""
    hp: int
    damage: int
    is_ex: bool = False
    attached_energy: int = 0
    card_type : str = "Pokemon"

    def __repr__(self):
        return f"Pokemon('{self.name}{'(ex)' if self.is_ex else ''}': HP = {self.hp}, damage = {self.damage}, {'attached energy = {self.attached_energy}' if self.attached_energy else 'no energy'}"

@dataclass
class Trainer(Card):
    """Trainer cards are non-Pokemon cards. Only one Supporter card may be played per turn"""
    is_supporter: bool = False
    description: str #will implement later
    card_type: str = "Trainer"