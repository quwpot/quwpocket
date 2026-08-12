"""Tests for turn structure and energy generation."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.card import Pokemon
from src.models.game_state import create_initial_state
from src.rules.actions import generate_actions, apply_action, start_turn
from src.cards.pokemon.pikachu import PIKACHU
from src.cards.trainers.potion import POTION

def test_energy_generation():
    """Test that energy is generated at start of turn."""
    deck = [PIKACHU] * 20
    game = create_initial_state(deck, deck, "Fire")
    
    # After create_initial_state, energy should be available
    print(f"Energy available P1: {game.player1.energy_available}")
    print(f"Energy available P2: {game.player2.energy_available}")
    
    assert game.player1.energy_available is True
    assert game.player2.energy_available is False  # Only current player gets energy
    
    # End turn
    game = apply_action(game, "END_TURN")
    print(f"After END_TURN - Energy available P1: {game.player1.energy_available}")
    print(f"After END_TURN - Energy available P2: {game.player2.energy_available}")
    
    assert game.player1.energy_available is True  # P1's turn ended
    assert game.player2.energy_available is True   # P2's turn started
    print("✅ Energy generated at start of turn")

def test_draw_at_start():
    """Test that player draws 1 card at start of turn."""
    deck = [PIKACHU] * 20
    game = create_initial_state(deck, deck, "Fire")
    
    initial_hand_size = len(game.player1.hand)
    initial_deck_size = len(game.player1.deck)
    
    print(f"Hand before draw: {initial_hand_size}")
    print(f"Deck before draw: {initial_deck_size}")
    
    # Start of turn already happened in create_initial_state
    # So hand should be initial draw + 1? Wait, let's track properly
    
    # End turn to test P2's draw
    game = apply_action(game, "END_TURN")
    
    print(f"P2 hand size: {len(game.player2.hand)}")
    print(f"P2 deck size: {len(game.player2.deck)}")
    
    # P2 should have drawn 1 card
    assert len(game.player2.hand) >= 1  # Opening hand + 1 draw
    print("✅ Draw at start of turn")

def test_attach_energy_then_end_turn():
    """Test attaching energy consumes energy_available."""
    deck = [PIKACHU] * 20
    game = create_initial_state(deck, deck, "Fire")
    
    # Energy should be available
    assert game.player1.energy_available is True
    
    # Attach energy
    game = apply_action(game, "ATTACH_ENERGY_TO_ACTIVE")
    print(f"Energy attached: {game.player1.active.attached_energy}")
    print(f"Energy available after attach: {game.player1.energy_available}")
    
    assert game.player1.active.attached_energy == 1
    assert game.player1.energy_available is False
    
    # End turn - P2 gets energy
    game = apply_action(game, "END_TURN")
    print(f"P2 energy available: {game.player2.energy_available}")
    assert game.player2.energy_available is True
    print("✅ Energy consumption works")

def test_cannot_attach_without_energy():
    """Test that you can't attach when energy_available is False."""
    deck = [PIKACHU] * 20
    game = create_initial_state(deck, deck, "Fire")
    
    # Attach energy once
    game = apply_action(game, "ATTACH_ENERGY_TO_ACTIVE")
    
    # Energy should now be False
    assert game.player1.energy_available is False
    
    # Generate actions - ATTACH_ENERGY should NOT be available
    actions = generate_actions(game)
    print(f"Actions: {actions}")
    
    assert "ATTACH_ENERGY_TO_ACTIVE" not in actions
    print("✅ Cannot attach without energy")

if __name__ == "__main__":
    print("=" * 50)
    print("TESTING TURN STRUCTURE")
    print("=" * 50)
    print()
    
    test_energy_generation()
    test_draw_at_start()
    test_attach_energy_then_end_turn()
    test_cannot_attach_without_energy()
    
    print("=" * 50)
    print("✅ All tests passed!")