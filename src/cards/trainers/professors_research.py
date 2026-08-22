from src.models.card import Trainer
from src.models.effect import Effect

# Create the card instance
PROFESSORS_RESEARCH = Trainer(
    name="Professors Research",
    card_type="trainer",
    is_supporter=True,
    effect=Effect(
        type="draw",
        amount=2,
    ),
    description="Draw 2 cards."
)