from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement

WEEDLE = Pokemon(
    name="Weedle",
    card_type="pokemon",
    typing="Grass",
    stage="basic",
    max_hp=50,
    hp=50,
    retreat_cost=1,
    weakness="Fire",
    evolves_from=None,
    is_ex=False,
    attacks=[
        Attack(
            name="Sting",
            damage=20,
            cost=[
                AttackRequirement("Grass", 1)
            ]
        )
    ]
)