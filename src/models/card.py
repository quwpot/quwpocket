from dataclasses import dataclass #dataclasses are classes for storing data (duh) and assist by automatically generating stuff like __init__ or __repr__
from src.models.effect import Effect

@dataclass
class Card:

    """
Basic class for all Cards.

Cards can be part of deck, hand or discard pile. They can also be in play.

Attributes:
    name: the displayed name
    card_type: either Pokemon or Trainer
    """

    name: str
    card_type: str

@dataclass
class Pokemon(Card):

    """
Class tracking all stats that makes a Pokemon unique.

Pokemons can attack, take damage and get KO'd. Energy cards may get attached to them as well.

Attributes:
    hp: current health points. start at max, decrease when damaged.
    damage: amount of hp enemy pokemon lose if they get attacked.
    stage: "basic", "stage1", "stage2" - shows where in the evolution line it is.
    evolves_from: the name of the immediate precedant in the evolution line.
    attack_cost: the amount of energy that needs to be attached in order for the pokemon to be able to use its attack and do damage.
    ex pokemon give two points when KO'd.
    retreat_cost: amount of energies that get discarded when switching this pokemon from the active spot to the bench.
    typing: "fire", "water", "grass", ... Important for calculating weakness later.
    turns_in_play: pokemon may only evolve if they've been in play for a full turn.
    attached_energy: amount of energy tokens (currency required to unleash attacks) are currently equipped. starts at 0 and increases as game progresses.
    """
    max_hp: int
    damage: int
    hp: int
    typing: str
    stage: str
    retreat_cost: int = 1
    weakness: str | None =  None
    evolves_from: str | None = None
    attack_cost: int = 0
    turns_in_play: int = 0
    is_ex: bool = False
    attached_energy: int = 0

    def __repr__(self):
        return f"Pokemon('{self.name}{'(ex)' if self.is_ex else ''}': HP = {self.hp}, damage = {self.damage}, {'attached energy = ' + str(self.attached_energy) if self.attached_energy else 'no energy'}"

@dataclass
class Trainer(Card):

    """
Trainer cards are non-Pokemon cards. Only one Supporter card may be played per turn
    """

    description: str
    effect: Effect
    is_supporter: bool = False