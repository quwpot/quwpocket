from src.models.card import Trainer
from src.models.effect import Effect

# Create the card instance
POTION = Trainer(
    name="Potion",
    card_type="trainer",
    is_supporter=False,
    effect=Effect(
        effect_type="heal",
        amount=20,
        target="any",  # Can target active or bench
        target_condition="healable"
    ),
    description="Heal 20 damage from 1 of your Pokémon."
)