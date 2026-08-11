"""Tests for knockout and scoring mechanics."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.card import Pokemon
from src.models.game_state import PlayerState, GameState
from src.rules.actions import apply_action, copy_state

def test_knockout_non_ex():
    """Test that knocking out a non-ex gives 1 point."""
    # Setup: attacker with damage, defender with low HP
    attacker = Pokemon(name="Pikachu", card_type="pokemon", hp=60, damage=30, attack_cost=1, attached_energy=1)
    defender = Pokemon(name="Pichu", card_type="pokemon", hp=20, damage=10, is_ex=False)
    
    p1 = PlayerState(active=attacker, energy_available=False)
    p2 = PlayerState(active=defender)
    
    game = GameState(
        player1=p1, player2=p2,
        turn=1, current_player=1,
        game_over=False, winner=None,
        supporter_played=False
    )
    
    # Attack
    new_game = apply_action(game, "ATTACK_WITH_ACTIVE")
    
    print(f"Points after KO: {new_game.player1.points}")
    print(f"Defender active: {new_game.player2.active}")
    
    assert new_game.player1.points == 1
    assert new_game.player2.active is None
    assert not new_game.game_over
    print("✅ Non-ex knockout gives 1 point")

def test_knockout_ex():
    """Test that knocking out an ex gives 2 points."""
    attacker = Pokemon(name="Charizard", card_type="pokemon", hp=180, damage=150, attack_cost=2, attached_energy=2, is_ex=True)
    defender = Pokemon(name="Pikachu", card_type="pokemon", hp=60, damage=20, is_ex=True)
    
    p1 = PlayerState(active=attacker, energy_available=False)
    p2 = PlayerState(active=defender)
    
    game = GameState(
        player1=p1, player2=p2,
        turn=1, current_player=1,
        game_over=False, winner=None,
        supporter_played=False
    )
    
    new_game = apply_action(game, "ATTACK_WITH_ACTIVE")
    
    print(f"Points after KO: {new_game.player1.points}")
    
    assert new_game.player1.points == 2
    print("✅ Ex knockout gives 2 points")

def test_game_end():
    """Test that reaching 3 points ends the game."""
    # Setup: player already has 2 points, knocks out an ex for 2 more
    attacker = Pokemon(name="Mewtwo", card_type="pokemon", hp=150, damage=120, attack_cost=2, attached_energy=2, is_ex=True)
    defender = Pokemon(name="Pikachu", card_type="pokemon", hp=60, damage=20, is_ex=True)
    
    p1 = PlayerState(active=attacker, points=2, energy_available=False)  # Already at 2 points
    p2 = PlayerState(active=defender)
    
    game = GameState(
        player1=p1, player2=p2,
        turn=1, current_player=1,
        game_over=False, winner=None,
        supporter_played=False
    )
    
    new_game = apply_action(game, "ATTACK_WITH_ACTIVE")
    
    print(f"Points after KO: {new_game.player1.points}")
    print(f"Game over: {new_game.game_over}")
    print(f"Winner: {new_game.winner}")
    
    assert new_game.game_over
    assert new_game.winner == 1
    print("✅ Game ends at 3 points")

if __name__ == "__main__":
    print("=" * 50)
    print("TESTING KNOCKOUT MECHANICS")
    print("=" * 50)
    print()
    
    test_knockout_non_ex()
    test_knockout_ex()
    test_game_end()
    
    print("=" * 50)
    print("✅ All tests passed!")