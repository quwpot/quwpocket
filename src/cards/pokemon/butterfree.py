from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement
from src.models.ability import Ability
from src.models.effect import Effect

BUTTERFREE = Pokemon(
    name="Butterfree",
    card_type="pokemon",
    typing="Grass",
    stage="stage2",
    max_hp=120,
    hp=120,
    retreat_cost=1,
    weakness="Fire",
    evolves_from="Metapod",
    is_ex=False,
    attacks=[
        Attack(
            name="Gust",
            damage=60,
            cost=[
                AttackRequirement("Grass", 1),
                AttackRequirement("Colorless", 2)
            ]
        )
    ],
    ability=Ability(
        name="Powder Heal",
        ability_type="once_per_turn",
        effect=Effect(
            effect_type="heal",
            amount=20,
            target="all_own",
        target_conditions=[
            {"type": "healable"},
        ],
        )
    )
)