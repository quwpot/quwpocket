from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement

IVYSAUR = Pokemon(
    name="Ivysaur",
    card_type="pokemon",
    typing="Grass",
    stage="stage1",
    max_hp=90,
    hp=90,
    retreat_cost=2,
    weakness="Fire",
    evolves_from="Bulbasaur",
    is_ex=False,
    attacks=[
        Attack(
            name="Razor Leaf",
            damage=60,
            cost=[
                AttackRequirement("Grass", 1),
                AttackRequirement("Colorless", 2)
            ]
        )
    ]
)