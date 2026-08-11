from src.models.card import Trainer
from src.models.effect import Effect

# Create the card instance
GIOVANNI = Trainer(
    name="Giovanni",
    card_type="trainer",
    is_supporter=True,
    effect=Effect(
        effect_type="damage_boost",
        amount=10
    ),
    description="During this turn, attacks used by your Pokémon do +10 damage to your opponent's Active Pokémon."
)