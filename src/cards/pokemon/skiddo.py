from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement
from src.models.effect import Effect

SKIDDO = Pokemon(
    name="Skiddo",
    card_type="pokemon",
    typing="Grass",
    stage="basic",
    max_hp=70,
    hp=70,
    retreat_cost=1,
    weakness="Fire",
    evolves_from=None,
    is_ex=False,
    attacks=[
        Attack(
            name="Surprise Attack",
            damage=40,
            cost=[
                AttackRequirement("Colorless", 1)
            ],
            effect=Effect(
                effect_type="coin_flip_bonus_damage",
                amount=1,
                instance=-40
            )
        )
    ]
)