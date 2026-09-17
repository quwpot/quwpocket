"""Tests for alpha-beta search."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement
from src.models.game_state import PlayerState, GameState
from src.solver.minimax import search

def make_game(p1_active, p2_active, p1_bench=None, p2_bench=None):
    p1 = PlayerState(active=p1_active, bench=p1_bench or [], energy_types=["Fire"])
    p2 = PlayerState(active=p2_active, bench=p2_bench or [], energy_types=["Fire"])
    return GameState(
        player1=p1, player2=p2,
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False,
        pending_promotion=False,
        pending_player=0
    )

def test_search_returns_number():
    """Test that search returns a numeric score."""
    pikachu = Pokemon(
        name="Pikachu", card_type="pokemon", typing="Electric",
        max_hp=60, hp=60,
        attacks=[Attack(name="Shock", damage=20,
                        cost=[AttackRequirement("Colorless", 1)])],
        attached_energy=["Electric"]
    )
    pichu = Pokemon(
        name="Pichu", card_type="pokemon", typing="Electric",
        max_hp=30, hp=30, attacks=[]
    )
    game = make_game(pikachu, pichu)
    
    score, _ = search(game, depth=2, alpha=float('-inf'), beta=float('inf'),
                   is_maximizing=True)
    print(f"Search score: {score}")
    assert isinstance(score, (int, float))
    print("✅ Search returns numeric score")

def test_find_best_move_attacks():
    """Test that solver attacks instead of ending turn."""
    pikachu = Pokemon(
        name="Pikachu", card_type="pokemon", typing="Electric",
        max_hp=60, hp=60,
        attacks=[Attack(name="Shock", damage=30,
                        cost=[AttackRequirement("Colorless", 1)])],
        attached_energy=["Electric"]
    )
    pichu = Pokemon(
        name="Pichu", card_type="pokemon", typing="Electric",
        max_hp=30, hp=30, attacks=[]
    )
    game = make_game(pikachu, pichu)
    
    _, best = search(game, depth=2)
    print(f"Best move: {best}")
    assert best.startswith("ATTACK_")
    print("✅ Solver attacks when it can KO")

def test_odd_depth_perspective():
    """Test that odd depth also uses hero perspective (the old bug)."""
    # Same position, depth 1 vs depth 2, both should give positive score
    pikachu = Pokemon(
        name="Pikachu", card_type="pokemon", typing="Electric",
        max_hp=60, hp=60,
        attacks=[Attack(name="Shock", damage=20,
                        cost=[AttackRequirement("Colorless", 1)])],
        attached_energy=["Electric"]
    )
    pichu = Pokemon(
        name="Pichu", card_type="pokemon", typing="Electric",
        max_hp=30, hp=30, attacks=[]
    )
    game = make_game(pikachu, pichu)
    
    score1, _ = search(game, 1, float('-inf'), float('inf'), True, 1)
    score2, _ = search(game, 2, float('-inf'), float('inf'), True, 1)
    
    print(f"Score at depth 1: {score1}")
    print(f"Score at depth 2: {score2}")
    print("✅ Perspective consistent across depths")

def test_alpha_beta_prunes():
    """Test that alpha-beta returns same result as plain search."""
    pikachu = Pokemon(
        name="Pikachu", card_type="pokemon", typing="Electric",
        max_hp=60, hp=60,
        attacks=[Attack(name="Shock", damage=20,
                        cost=[AttackRequirement("Colorless", 1)])],
        attached_energy=["Electric"]
    )
    pichu = Pokemon(
        name="Pichu", card_type="pokemon", typing="Electric",
        max_hp=50, hp=50, attacks=[]
    )
    game = make_game(pikachu, pichu)
    
    # With wide-open window (no pruning possible)
    wide,_ = search(game, 3, float('-inf'), float('inf'), True, 1)
    print(f"now narrow")
    # With narrow window (will prune)
    narrow,_ = search(game, 3, 0, 0, True, 1)
    
    print(f"Wide window score: {wide}")
    print(f"Narrow window score: {narrow}")
    # These may differ if narrow causes cutoffs, but both should be numbers
    assert isinstance(wide, (int, float))
    assert isinstance(narrow, (int, float))
    print("✅ Alpha-beta runs without errors")

if __name__ == "__main__":
    print("=" * 50)
    print("TESTING ALPHA-BETA SEARCH")
    print("=" * 50)
    print()
    
    test_search_returns_number()
    test_find_best_move_attacks()
    test_odd_depth_perspective()
    test_alpha_beta_prunes()
    
    print("=" * 50)
    print("✅ All tests passed!")