"""Tests for first turn restrictions."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.card import Pokemon
from src.models.game_state import create_initial_state
from src.rules.actions import generate_actions, apply_action, start_turn
from src.cards.pokemon.pikachu import PIKACHU
from src.cards.trainers.potion import POTION

def test_first_player_no_energy():
    """Test that Player 1 gets no energy on first turn."""
    deck = [PIKACHU] * 20
    game = create_initial_state(deck, deck, "Fire", debug=True)
    
    print(f"Player 1 energy available: {game.player1.energy_available}")
    print(f"Game first_turn flag: {game.is_first_turn}")
    
    # Player 1 should have NO energy on first turn
    assert game.player1.energy_available is False
    print("✅ Player 1 has no energy on first turn")

def test_second_player_has_energy():
    """Test that Player 2 gets energy on their first turn."""
    deck = [PIKACHU] * 20
    game = create_initial_state(deck, deck, "Fire")
    
    # End Player 1's turn
    game = apply_action(game, "END_TURN")
    
    print(f"Player 2 energy available: {game.player2.energy_available}")
    print(f"Game first_turn flag: {game.is_first_turn}")
    
    # Player 2 should have energy
    assert game.player2.energy_available is True
    assert game.is_first_turn is False
    print("✅ Player 2 has energy on first turn")

def test_second_turn_player_1_has_energy():
    """Test that Player 1 gets energy on their second turn."""
    deck = [PIKACHU] * 20
    game = create_initial_state(deck, deck, "Fire")
    
    # Complete Player 1's turn (no energy)
    game = apply_action(game, "END_TURN")  # Player 2's turn starts
    game = apply_action(game, "END_TURN")  # Player 1's second turn starts
    
    print(f"Player 1 energy available: {game.player1.energy_available}")
    print(f"Game first_turn flag: {game.is_first_turn}")
    
    # Player 1 should now have energy
    assert game.player1.energy_available is True
    assert game.is_first_turn is False
    print("✅ Player 1 has energy on second turn")

def test_attach_energy_not_available_first_turn():
    """Test that ATTACH_ENERGY is not available on first turn."""
    deck = [PIKACHU] * 20
    game = create_initial_state(deck, deck, "Fire")
    
    actions = generate_actions(game)
    print(f"Actions on first turn: {actions}")
    
    assert "ATTACH_ENERGY_TO_ACTIVE" not in actions
    print("✅ Cannot attach energy on first turn")

def test_attack_available_first_turn():
    """Test that attack IS available on first turn (in your rules)."""
    deck = [PIKACHU] * 20
    game = create_initial_state(deck, deck, "Fire")
    
    # Give Pikachu energy (even though no generation, we'll manually attach for test)
    # Actually, in your rules, you said attacking is allowed - let's just check action exists
    
    # First turn actions should include ATTACK_WITH_ACTIVE if active has energy
    # But active won't have energy on first turn...
    # So this test needs a different setup
    
    # Let's just test that attack is in the action list when energy exists
    # We'll simulate by giving Pikachu energy directly
    game.player1.active.attached_energy = 1
    
    actions = generate_actions(game)
    print(f"Actions with energy: {actions}")
    
    assert "ATTACK_WITH_ACTIVE" in actions
    print("✅ Attack available on first turn (with energy from cards like Energy Search)")

if __name__ == "__main__":
    print("=" * 50)
    print("TESTING FIRST TURN RULES")
    print("=" * 50)
    print()
    
    test_first_player_no_energy()
    test_second_player_has_energy()
    test_second_turn_player_1_has_energy()
    test_attach_energy_not_available_first_turn()
    test_attack_available_first_turn()
    
    print("=" * 50)
    print("✅ All tests passed!")