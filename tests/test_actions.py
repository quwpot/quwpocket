"""Tests for game actions."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.card import Pokemon
from src.models.game_state import PlayerState, GameState, create_initial_state
from src.rules.actions import generate_actions, apply_action

def test_action_generation():
    """Test that actions are generated correctly."""
    # Create a state with a Pokemon in play
    pikachu = Pokemon(name="Pikachu", card_type="pokemon", hp=60, damage=20)
    player = PlayerState(active=pikachu, energy_available=True)
    game = GameState(
        player1=player,
        player2=PlayerState(),
        turn=1,
        current_player=1,
        game_over=False,
        winner=None,
        supporter_played=False
    )
    
    actions = generate_actions(game)
    print(f"Generated actions: {actions}")
    
    # We should have at least END_TURN, ATTACH, and ATTACK
    assert "END_TURN" in actions
    assert "ATTACH_ENERGY_TO_ACTIVE" in actions
    assert "ATTACK_WITH_ACTIVE" in actions
    
    print("✅ Action generation test passed!")

def test_end_turn():
    """Test that END_TURN switches players correctly."""
    game = create_initial_state("Fire")
    print(f"Before end turn: Player {game.current_player}'s turn")
    
    new_game = apply_action(game, "END_TURN")
    print(f"After end turn: Player {new_game.current_player}'s turn")
    
    assert new_game.current_player != game.current_player
    assert new_game.turn == game.turn + 1
    print("✅ END_TURN test passed!")

def test_attach_energy():
    """Test that energy attachment works."""
    pikachu = Pokemon(name="Pikachu", card_type="pokemon", hp=60, damage=20, attached_energy=0)
    player = PlayerState(active=pikachu, energy_available=True)
    game = GameState(
        player1=player,
        player2=PlayerState(),
        turn=1,
        current_player=1,
        game_over=False,
        winner=None,
        supporter_played=False
    )
    
    print(f"Before attach: {game.player1.active}")
    new_game = apply_action(game, "ATTACH_ENERGY_TO_ACTIVE")
    print(f"After attach: {new_game.player1.active}")
    
    assert new_game.player1.active.attached_energy == 1
    assert new_game.player1.energy_available is False
    print("✅ Energy attachment test passed!")

if __name__ == "__main__":
    print("=" * 50)
    print("TESTING GAME ACTIONS")
    print("=" * 50)
    print()
    
    test_action_generation()
    test_end_turn()
    test_attach_energy()
    
    print("=" * 50)
    print("✅ All tests passed!")