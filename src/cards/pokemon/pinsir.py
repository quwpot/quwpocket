from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement
from src.models.effect import Effect

PINSIR = Pokemon(
    name="Pinsir",
    card_type="pokemon",
    typing="Grass",
    stage="basic",
    max_hp=70,
    hp=70,
    retreat_cost=2,
    weakness="Fire",
    evolves_from=None,
    is_ex=False,
    attacks=[
        Attack(
            name="Double Horn",
            damage=0,
            cost=[
                AttackRequirement("Grass", 2)
            ],
            effect=Effect(
                effect_type="coin_flip_bonus_damage",
                amount=2,
                instance=50
            )
        )
    ]
)