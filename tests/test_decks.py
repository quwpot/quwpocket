"""Tests for Pokemon cards and deck building."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cards.pokemon.pikachu import PIKACHU
from src.cards.pokemon.bulbasaur import BULBASAUR
from src.rules.deck_builder import build_deck
from src.models.game_state import create_initial_state

def test_pokemon_creation():
    """Test that Pokemon cards are created correctly."""
    print(f"Pikachu: {PIKACHU}")
    print(f"Bulbasaur: {BULBASAUR}")
    
    assert PIKACHU.name == "Pikachu"
    assert PIKACHU.typing == "Electric"
    assert PIKACHU.hp == 60
    print("✅ Pokemon cards work")

def test_deck_building():
    """Test building a deck from card names."""
    deck_list = ["Pikachu", "Bulbasaur", "Pikachu", "Bulbasaur"]
    deck = build_deck(deck_list)
    
    print(f"Deck size: {len(deck)}")
    print(f"First card: {deck[0].name}")
    assert len(deck) == 4
    assert deck[0].name == "Pikachu"
    print("✅ Deck building works")

def test_initial_state_with_deck():
    """Test creating initial state with decks."""
    p1_deck = ["Pikachu", "Bulbasaur"] * 10  # 20 cards
    p2_deck = ["Charmander", "Squirtle"] * 10  # 20 cards
    
    game = create_initial_state(
        energy_type="Fire",
        player1_deck=build_deck(p1_deck),
        player2_deck=build_deck(p2_deck)
    )
    
    print(f"Player1 deck size: {len(game.player1.deck)}")
    print(f"Player1 hand size: {len(game.player1.hand)}")
    print(f"Player1 energy type: {game.player1.energy_type}")
    
    # Should have 15 cards left in deck (20 - 5 drawn)
    assert len(game.player1.deck) == 15
    assert len(game.player1.hand) == 4
    print("✅ Initial state with decks works")

if __name__ == "__main__":
    print("=" * 50)
    print("TESTING POKEMON AND DECKS")
    print("=" * 50)
    print()
    
    test_pokemon_creation()
    test_deck_building()
    test_initial_state_with_deck()
    
    print("=" * 50)
    print("✅ All tests passed!")