from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement
from src.models.effect import Effect

PETILIL = Pokemon(
    name="Petilil",
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
            name="Blot",
            damage=10,
            cost=[
                AttackRequirement("Grass", 1)
            ],
            effect=Effect(
                effect_type="heal",
                amount=10,
                target="active"
            )
        )
    ]
)