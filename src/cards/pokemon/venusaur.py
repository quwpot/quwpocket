from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement
from src.models.effect import Effect

VENUSAUR = Pokemon(
    name="Venusaur",
    card_type="pokemon",
    typing="Grass",
    stage="stage2",
    max_hp=160,
    hp=160,
    retreat_cost=3,
    weakness="Fire",
    evolves_from="Ivysaur",
    is_ex=False,
    attacks=[
        Attack(
            name="Mega Drain",
            damage=80,
            cost=[
                AttackRequirement("Grass", 2),
                AttackRequirement("Colorless", 2)
            ],
            effect=Effect(
                type="heal",
                amount=30,
                target="active"
            )
        )
    ]
)