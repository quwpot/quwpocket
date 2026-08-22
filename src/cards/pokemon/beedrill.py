from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement

BEEDRILL = Pokemon(
    name="Beedrill",
    card_type="pokemon",
    typing="Grass",
    stage="stage2",
    max_hp=120,
    hp=120,
    retreat_cost=1,
    weakness="Fire",
    evolves_from="Kakuna",
    is_ex=False,
    attacks=[
        Attack(
            name="Sharp Sting",
            damage=70,
            cost=[
                AttackRequirement("Grass", 1)
            ]
        )
    ]
)