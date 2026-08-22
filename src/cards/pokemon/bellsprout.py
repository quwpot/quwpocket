from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement

BELLSPROUT = Pokemon(
    name="Bellsprout",
    card_type="pokemon",
    typing="Grass",
    stage="basic",
    max_hp=60,
    hp=60,
    retreat_cost=1,
    weakness="Fire",
    evolves_from=None,
    is_ex=False,
    attacks=[
        Attack(
            name="Vine Whip",
            damage=20,
            cost=[
                AttackRequirement("Grass", 1)
            ]
        )
    ]
)