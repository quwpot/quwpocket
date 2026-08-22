from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement
from src.models.effect import Effect

TANGELA = Pokemon(
    name="Tangela",
    card_type="pokemon",
    typing="Grass",
    stage="basic",
    max_hp=80,
    hp=80,
    retreat_cost=2,
    weakness="Fire",
    evolves_from=None,
    is_ex=False,
    attacks=[
        Attack(
            name="Absorb",
            damage=40,
            cost=[
                AttackRequirement("Grass", 1),
                AttackRequirement("Colorless", 1)
            ],
            effect=Effect(
                effect_type="heal",
                amount=10,
                target="active"
            )
        )
    ]
)