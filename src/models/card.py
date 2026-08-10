from dataclasses import dataclass #dataclasses are classes for storing data (duh) and assist by automatically generating stuff like __init__ or __repr__

@dataclass
class Card:
"""Basic class for all Cards"""
    name: str
    card_type: str

@dataclass
class Pokemon:
"""Class tracking all stats that makes a Pokemon unique"""
#some inheritance shenanigans
    hp: int
    damage: int
    is_ex: bool = False
    attached_energy: int = 0

    def __repr__(self):
        return f"Pokemon('{self.name}{if self.is_ex: (ex)}': HP = {self.hp}, damage = {self.damage}, attached energy = {self.attached_energy}"

@dataclass
class Trainer:
"""Trainer cards are non-Pokemon cards. Only one Supporter card may be played per turn"""
#again inheritance
    is_supporter: bool = False
    description: str #will implement later

@dataclass
class Energyzone: #correct file?
"""Energy types are set based on the deck. Unused Energy is lost and can't be 'saved' for later."""
    energy_type: str
    next_type: str
    empty: bool = False