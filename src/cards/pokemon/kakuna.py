from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement

KAKUNA = Pokemon(
    name="Kakuna",
    card_type="pokemon",
    typing="Grass",
    stage="stage1",
    max_hp=80,
    hp=80,
    retreat_cost=2,
    weakness="Fire",
    evolves_from="Weedle",
    is_ex=False,
    attacks=[
        Attack(
            name="Bug Bite",
            damage=30,
            cost=[
                AttackRequirement("Grass", 1)
            ]
        )
    ]
)