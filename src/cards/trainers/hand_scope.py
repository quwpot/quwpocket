from src.models.card import Trainer
from src.models.effect import Effect

# Create the card instance
HAND_SCOPE = Trainer(
    name="Hand Scope",
    card_type="trainer",
    is_supporter=False,
    effect=Effect(
        effect_type="watch_opponent_hand_cards",
        amount=10,
    ),
    description="Your opponent reveals their hand."
)