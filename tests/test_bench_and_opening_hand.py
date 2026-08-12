"""Tests for bench placement and opening hand."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.card import Pokemon, Trainer
from src.models.game_state import create_initial_state
from src.rules.actions import generate_actions, apply_action
from src.cards.pokemon.pikachu import PIKACHU
from src.cards.pokemon.bulbasaur import BULBASAUR
from src.cards.trainers.potion import POTION

def test_opening_hand_has_pokemon():
    """Test that opening hand always has at least one Pokemon."""
    deck = [PIKACHU, POTION, POTION, POTION, POTION, PIKACHU, PIKACHU, PIKACHU] * 3  # 24 cards
    game = create_initial_state(deck, deck, "Fire", debug=True)
    
    print(f"Player1 hand: {[card.name for card in game.player1.hand]}")
    print(f"Player1 active: {game.player1.active.name if game.player1.active else 'None'}")
    
    assert game.player1.active is not None
    assert len(game.player1.hand) == 4  # 1 basic + 4 drawn
    print("✅ Opening hand has Pokemon")

def test_play_pokemon_to_bench():
    """Test playing a Pokemon from hand to bench."""
    # Setup: Player has hand with Pikachu and empty bench
    deck = [PIKACHU, PIKACHU, PIKACHU, PIKACHU] * 2  # 4 Pikachus
    game = create_initial_state(deck, deck, "Fire", debug=True)
    
    # Get current player
    player = game.player1
    
    # There should be a Pikachu in hand (in addition to active)
    print(f"Hand before: {[card.name for card in player.hand]}")
    
    # Find action to play Pikachu (should be PLAY_CARD_0 since it's first in hand)
    actions = generate_actions(game, debug=True)
    play_action = None
    for action in actions:
        if action.startswith("PLAY_CARD_"):
            card_index = int(action.split("_")[-1])
            card = player.hand[card_index]
            if card.name == "Pikachu":
                play_action = action
                break
    
    if play_action:
        new_game = apply_action(game, play_action)
        print(f"Bench size after: {len(new_game.player1.bench)}")
        print(f"Hand after: {[card.name for card in new_game.player1.hand]}")
        assert len(new_game.player1.bench) == 1
        assert new_game.player1.bench[0].name == "Pikachu"
        print("✅ Pokemon played to bench")
    else:
        print("error")

def test_bench_limit():
    """Test that bench can't exceed 3 Pokemon."""
    deck = [PIKACHU, PIKACHU, PIKACHU, PIKACHU, PIKACHU]  # 5 Pikachus
    game = create_initial_state(deck, deck, "Fire")
    player = game.player1
    
    # Play 3 Pikachus to bench (should be possible)
    for i in range(3):
        actions = generate_actions(game, debug=True)
        for action in actions:
            if action.startswith("PLAY_CARD_"):
                game = apply_action(game, action)
                print(i)
                break
    
    print(f"Bench size after 3 plays: {len(game.player1.bench)}")
    assert len(game.player1.bench) == 3
    
    # Try to play 4th (should not be possible)
    actions = generate_actions(game)
    play_actions = [a for a in actions if a.startswith("PLAY_CARD_")]
    print(f"Play actions available: {len(play_actions)}")
    
    # Should only have 2 play actions (the 2 Pikachus still in hand, but bench is full)
    assert len(play_actions) == 0  # The 2 remaining Pikachus, but can't play due to full bench
    print("✅ Bench limit enforced")

if __name__ == "__main__":
    print("=" * 50)
    print("TESTING BENCH AND OPENING HAND")
    print("=" * 50)
    print()
    
    test_opening_hand_has_pokemon()
    test_play_pokemon_to_bench()
    test_bench_limit()
    
    print("=" * 50)
    print("✅ All tests passed!")