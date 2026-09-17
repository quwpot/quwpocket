from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement
from src.models.effect import Effect

VILEPLUME = Pokemon(
    name="Vileplume",
    card_type="pokemon",
    typing="Grass",
    stage="stage2",
    max_hp=140,
    hp=140,
    retreat_cost=3,
    weakness="Fire",
    evolves_from="Gloom",
    is_ex=False,
    attacks=[
        Attack(
            name="Soothing Scent",
            damage=80,
            cost=[
                AttackRequirement("Grass", 2),
                AttackRequirement("Colorless", 1)
            ],
            effect=Effect(
                effect_type="special_condition",
                instance="sleep",
                target="opponent"
            )
        )
    ]
)