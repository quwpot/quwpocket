from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement

VICTREEBELL = Pokemon(
    name="Victreebell",
    card_type="pokemon",
    typing="Grass",
    stage="stage2",
    max_hp=140,
    hp=140,
    retreat_cost=2,
    weakness="Fire",
    evolves_from="Weepinbell",
    is_ex=False,
    attacks=[
        Attack(
            name="Vine Whip",
            damage=60,
            cost=[
                AttackRequirement("Grass", 1),
                AttackRequirement("Colorless", 1)
            ]
        )
    ]
)