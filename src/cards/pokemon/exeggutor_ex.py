from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement
from src.models.effect import Effect

EXEGGUTOR_EX = Pokemon(
    name="Exeggutor ex",
    card_type="pokemon",
    typing="Grass",
    stage="stage1",
    max_hp=160,
    hp=160,
    retreat_cost=3,
    weakness="Fire",
    evolves_from="Exeggcute",
    is_ex=True,
    attacks=[
        Attack(
            name="Tropical Swing",
            damage=40,
            cost=[
                AttackRequirement("Grass", 1)
            ],
            effect=Effect(
                effect_type="coin_flip_bonus_damage",
                amount=1,
                instance=40
            )
        )
    ]
)