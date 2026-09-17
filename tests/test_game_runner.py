"""Tests for the game runner."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.solver.game_runner import play_game

def test_full_game_runs():
    """Test that a full game runs without errors."""
    
    result = play_game(solver_depth=2, max_turns=30)
    
    print(f"\nFinal result: {result}")
    assert result is not None
    assert "winner" in result or "turns" in result
    print("✅ Full game completed")

if __name__ == "__main__":
    print("=" * 50)
    print("TESTING GAME RUNNER")
    print("=" * 50)
    print()
    
    test_full_game_runs()
    
    print("=" * 50)
    print("✅ Test passed!")