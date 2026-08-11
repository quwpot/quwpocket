from src.cards.registry import get_card

def build_deck(card_names: list[str]) -> list:
    """Build a deck from a list of card names."""
    deck = []
    for name in card_names:
        card = get_card(name)
        if card:
            deck.append(card)
        else:
            print(f"Warning: {name} not found in registry")
    return deck