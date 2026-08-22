from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement

GOGOAT = Pokemon(
    name="Gogoat",
    card_type="pokemon",
    typing="Grass",
    stage="stage1",
    max_hp=120,
    hp=120,
    retreat_cost=2,
    weakness="Fire",
    evolves_from="Skiddo",
    is_ex=False,
    attacks=[
        Attack(
            name="Razor Leaf",
            damage=70,
            cost=[
                AttackRequirement("Grass", 1),
                AttackRequirement("Colorless", 2)
            ]
        )
    ]
)