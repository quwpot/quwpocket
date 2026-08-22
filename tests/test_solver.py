"""Tests for the solver."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement
from src.models.game_state import PlayerState, GameState
from src.solver.minimax import find_best_move
from src.rules.actions import apply_action

def test_solver_finds_winning_move():
    """Test that solver finds the obvious winning move."""
    # Setup: Attacker can win by attacking
    pikachu = Pokemon(
        name="Pikachu",
        card_type="pokemon",
        typing="Electric",
        max_hp=60, hp=60,
        attacks=[
            Attack(
                name="Thunder Shock",
                damage=30,
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
    
    # Find best move
    best_action = find_best_move(game, depth=3)
    print(f"Best action: {best_action}")
    
    # Should choose to attack (not end turn)
    assert best_action.startswith("ATTACK_")
    print("✅ Solver finds winning attack")

if __name__ == "__main__":
    print("=" * 50)
    print("TESTING SOLVER")
    print("=" * 50)
    print()
    
    test_solver_finds_winning_move()
    
    print("=" * 50)
    print("✅ All tests passed!")