from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement

PIKACHU = Pokemon(
    name="Pikachu",
    card_type="pokemon",
    typing="Electric",
    stage="basic",
    max_hp=60,
    hp=60,
    retreat_cost=1,
    weakness="Fighting",
    evolves_from=None,
    is_ex=False,
    attacks=[
        Attack(
            name="Gnaw",
            damage=20,
            cost=[
                AttackRequirement("Electric", 1)
            ]
        )
    ]
)