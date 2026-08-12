from src.models.card import Pokemon

CHARMANDER = Pokemon(
    name="Charmander",
    card_type="pokemon",
    typing="Fire",
    stage="basic",
    max_hp=60,
    hp=60,
    damage=30,
    attack_cost=1,
    retreat_cost=1,
    weakness="Water",
    is_ex=False
)