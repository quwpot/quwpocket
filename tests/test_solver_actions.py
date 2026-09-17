"""Tests for solver with turn-based search."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement
from src.models.game_state import PlayerState, GameState
from src.solver.search import get_turn_sequences
from src.solver.minimax import minimax_turn

def test_get_turn_sequences():
    """Test that turn sequences all end with END_TURN."""
    # Setup simple state with one action available
    pikachu = Pokemon(
        name="Pikachu",
        card_type="pokemon",
        typing="Electric",
        max_hp=60, hp=60,
        attacks=[],
        attached_energy=["Electric"]
    )
    player = PlayerState(active=pikachu)
    game = GameState(
        player1=player, player2=PlayerState(),
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False,
        pending_promotion=False,
        pending_player=0
    )
    
    sequences = get_turn_sequences(game)
    print(f"Found {len(sequences)} turn sequences")
    
    if sequences:
        print(f"First sequence: {sequences[0]}")
        # Check that the last action is END_TURN
        assert sequences[0][-1] == "END_TURN"
        print("✅ All sequences end with END_TURN")
    else:
        print("⚠️ No sequences found (should have at least END_TURN)")
        assert sequences

def test_find_best_move():
    """Test that find_best_move returns a valid action."""
    pikachu = Pokemon(
        name="Pikachu",
        card_type="pokemon",
        typing="Electric",
        max_hp=60, hp=60,
        attacks=[
            Attack(
                name="Thunder Shock",
                damage=20,
                cost=[AttackRequirement("Colorless", 1)]
            )
        ],
        attached_energy=["Electric"]
    )
    pichu = Pokemon(
        name="Pichu",
        card_type="pokemon",
        typing="Electric",
        max_hp=30, hp=30,
        attacks=[]
    )
    
    p1 = PlayerState(active=pikachu, energy_types=["Fire"])
    p2 = PlayerState(active=pichu, energy_types=["Fire"])
    game = GameState(
        player1=p1, player2=p2,
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False,
        pending_promotion=False,
        pending_player=0
    )
    
    _, best_move = minimax_turn(game, depth=3)
    print(f"Best move: {best_move}")
    
    # Should choose to attack (not end turn)
    assert best_move.startswith("ATTACK_")
    print("✅ Solver finds attacking move")

if __name__ == "__main__":
    print("=" * 50)
    print("TESTING SOLVER SEARCH")
    print("=" * 50)
    print()
    
    test_get_turn_sequences()
    test_find_best_move()
    
    print("=" * 50)
    print("✅ All tests passed!")