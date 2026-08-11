"""Tests for attack energy requirements."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.card import Pokemon
from src.models.game_state import PlayerState, GameState
from src.rules.actions import generate_actions

def test_attack_without_energy():
    """Attack should NOT be available without enough energy."""
    pikachu = Pokemon(
        name="Pikachu", 
        card_type="pokemon", 
        hp=60, 
        damage=20,
        attack_cost=1,
        attached_energy=0  # No energy
    )
    
    player = PlayerState(active=pikachu)
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
    print(f"Actions without energy: {actions}")
    
    assert "ATTACK_WITH_ACTIVE" not in actions
    print("✅ Attack correctly blocked when energy insufficient")

def test_attack_with_energy():
    """Attack should be available with enough energy."""
    pikachu = Pokemon(
        name="Pikachu", 
        card_type="pokemon", 
        hp=60, 
        damage=20,
        attack_cost=1,
        attached_energy=1  # Enough energy!
    )
    
    player = PlayerState(active=pikachu)
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
    print(f"Actions with energy: {actions}")
    
    assert "ATTACK_WITH_ACTIVE" in actions
    print("✅ Attack available with sufficient energy")

def test_attack_with_exact_cost():
    """Attack should work with exact energy cost."""
    charizard = Pokemon(
        name="Charizard", 
        card_type="pokemon", 
        hp=180, 
        damage=150,
        attack_cost=2,
        attached_energy=2  # Exactly enough
    )
    
    player = PlayerState(active=charizard)
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
    print(f"Actions with exact cost: {actions}")
    
    assert "ATTACK_WITH_ACTIVE" in actions
    print("✅ Attack available with exact energy cost")

if __name__ == "__main__":
    print("=" * 50)
    print("TESTING ATTACK REQUIREMENTS")
    print("=" * 50)
    print()
    
    test_attack_without_energy()
    test_attack_with_energy()
    test_attack_with_exact_cost()
    
    print("=" * 50)
    print("✅ All tests passed!")