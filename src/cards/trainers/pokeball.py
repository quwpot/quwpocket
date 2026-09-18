from src.models.card import Trainer
from src.models.effect import Effect

POKEBALL = Trainer(
    name="Pokeball",
    card_type="trainer",
    is_supporter=False,
    effect=Effect(
        effect_type="deck_to_hand",
        amount=1,
        target_conditions=[
            {"type": "stage", "value": "basic"},
        ],
    )
)