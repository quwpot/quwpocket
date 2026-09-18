from src.models.card import Trainer
from src.models.effect import Effect

# Create the card instance
ERIKA = Trainer(
    name="Erika",
    card_type="trainer",
    is_supporter=True,
    effect=Effect(
        effect_type="heal",
        amount=50,
        target="any",
        target_conditions=[
            {"type": "typing", "value": "Grass"},
            {"type": "healable"},
        ],
    ),
    description="Heal 50 damage from 1 of your Grass-Type Pokémon."
)