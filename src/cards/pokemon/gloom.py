from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement

GLOOM = Pokemon(
    name="Gloom",
    card_type="pokemon",
    typing="Grass",
    stage="stage1",
    max_hp=80,
    hp=80,
    retreat_cost=2,
    weakness="Fire",
    evolves_from="Oddish",
    is_ex=False,
    attacks=[
        Attack(
            name="Drool",
            damage=40,
            cost=[
                AttackRequirement("Grass", 1),
                AttackRequirement("Colorless", 1)
            ]
        )
    ]
)