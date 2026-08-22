from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement

WHIMSICOTT = Pokemon(
    name="Whimsicott",
    card_type="pokemon",
    typing="Grass",
    stage="stage1",
    max_hp=80,
    hp=80,
    retreat_cost=1,
    weakness="Fire",
    evolves_from="Cottonee",
    is_ex=False,
    attacks=[
        Attack(
            name="Rolling Tackle",
            damage=40,
            cost=[
                AttackRequirement("Colorless", 1)
            ]
        )
    ]
)