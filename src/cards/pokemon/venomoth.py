from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement

VENOMOTH = Pokemon(
    name="Venomoth",
    card_type="pokemon",
    typing="Grass",
    stage="stage1",
    max_hp=80,
    hp=80,
    retreat_cost=1,
    weakness="Fire",
    evolves_from="Venonat",
    is_ex=False,
    attacks=[
        Attack(
            name="Poison Powder",
            damage=30,
            cost=[
                AttackRequirement("Grass", 1)
            ]
        )
    ]
)