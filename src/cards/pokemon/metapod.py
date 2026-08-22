from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement

METAPOD = Pokemon(
    name="Metapod",
    card_type="pokemon",
    typing="Grass",
    stage="stage1",
    max_hp=80,
    hp=80,
    retreat_cost=2,
    weakness="Fire",
    evolves_from="Caterpie",
    is_ex=False,
    attacks=[
        Attack(
            name="Bug Bite",
            damage=30,
            cost=[
                AttackRequirement("Colorless", 2)
            ]
        )
    ]
)