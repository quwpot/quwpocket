from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement

SKIDDO = Pokemon(
    name="Skiddo",
    card_type="pokemon",
    typing="Grass",
    stage="basic",
    max_hp=70,
    hp=70,
    retreat_cost=1,
    weakness="Fire",
    evolves_from=None,
    is_ex=False,
    attacks=[
        Attack(
            name="Surprise Attack",
            damage=40,
            cost=[
                AttackRequirement("Colorless", 1)
            ]
        )
    ]
)