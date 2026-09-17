from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement
from src.models.effect import Effect

EXEGGUTOR = Pokemon(
    name="Exeggutor",
    card_type="pokemon",
    typing="Grass",
    stage="stage1",
    max_hp=130,
    hp=130,
    retreat_cost=3,
    weakness="Fire",
    evolves_from="Exeggcute",
    is_ex=False,
    attacks=[
        Attack(
            name="Stomp",
            damage=30,
            cost=[
                AttackRequirement("Grass", 1)
            ],
            effect=Effect(
                effect_type="coin_flip_bonus_damage",
                amount=1,
                instance=30
            )
        )
    ]
)