from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement

PARASECT = Pokemon(
    name="Parasect",
    card_type="pokemon",
    typing="Grass",
    stage="stage1",
    max_hp=120,
    hp=120,
    retreat_cost=2,
    weakness="Fire",
    evolves_from="Paras",
    is_ex=False,
    attacks=[
        Attack(
            name="Slash",
            damage=80,
            cost=[
                AttackRequirement("Grass", 2),
                AttackRequirement("Colorless", 1)
            ]
        )
    ]
)