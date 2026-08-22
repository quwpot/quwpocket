from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement
from src.models.effect import Effect

CATERPIE = Pokemon(
    name="Caterpie",
    card_type="pokemon",
    typing="Grass",
    stage="basic",
    max_hp=50,
    hp=50,
    retreat_cost=1,
    weakness="Fire",
    evolves_from=None,
    is_ex=False,
    attacks=[
        Attack(
            name="Find a Friend",
            damage=0,
            cost=[
                AttackRequirement("Colorless", 1)
            ],
            effect=Effect(
                effect_type="deck_to_hand",
                amount=1,
                target_condition="typing",
                target_condition_instance="Grass"
            )
        )
    ]
)