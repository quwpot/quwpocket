from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement

VENUSAUR EX = Pokemon(
    name="Venusaur ex",
    card_type="pokemon",
    typing="Grass",
    stage="stage2",
    max_hp=190,
    hp=190,
    retreat_cost=3,
    weakness="Fire",
    evolves_from=evolves_from,
    is_ex=True,
    attacks=[
        Attack(
            name="Razor Leaf",
            damage=60,
            cost=[
                AttackRequirement("Grass", 1),
                AttackRequirement("Colorless", 2),
                AttackRequirement("Grass", 2),
                AttackRequirement("Colorless", 2)
            ]
        ),
        Attack(
            name="Giant Bloom",
            damage=100,
            cost=[
                AttackRequirement("Grass", 1),
                AttackRequirement("Colorless", 2),
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