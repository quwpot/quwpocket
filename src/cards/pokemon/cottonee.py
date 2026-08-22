from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement

COTTONEE = Pokemon(
    name="Cottonee",
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
            name="Attach",
            damage=10,
            cost=[
                AttackRequirement("Colorless", 1)
            ]
        )
    ]
)