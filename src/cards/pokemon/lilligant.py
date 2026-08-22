from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement

LILLIGANT = Pokemon(
    name="Lilligant",
    card_type="pokemon",
    typing="Grass",
    stage="stage1",
    max_hp=100,
    hp=100,
    retreat_cost=1,
    weakness="Fire",
    evolves_from="Petilil",
    is_ex=False,
    attacks=[
        Attack(
            name="Leaf Supply",
            damage=50,
            cost=[
                AttackRequirement("Grass", 2)
            ],
            effect=Effect(
                effect_type="attach_energy",
                amount=1,
                instance="Grass",
                target="bench"
            )
        )
    ]
)