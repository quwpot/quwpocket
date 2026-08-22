from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement

SCYTHER = Pokemon(
    name="Scyther",
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
            name="Sharp Scythe",
            damage=30,
            cost=[
                AttackRequirement("Grass", 1)
            ]
        )
    ]
)