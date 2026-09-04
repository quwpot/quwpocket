from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement

VENONAT = Pokemon(
    name="Venonat",
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
            name="Tackle",
            damage=20,
            cost=[
                AttackRequirement("Grass", 1)
            ],
            effect=Effect(
                effect_type="special_condition",
                instance="poison",
                target="opponent"
            )
        )
    ]
)