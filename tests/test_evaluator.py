"""Tests for the evaluator function."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.card import Pokemon
from src.models.game_state import PlayerState, GameState
from src.solver.evaluator import evaluate_state
from src.cards.pokemon.caterpie import CATERPIE

def test_evaluation_basic():
    """Test that evaluation returns a number."""
    pikachu = Pokemon(
        name="Pikachu",
        card_type="pokemon",
        typing="Electric",
        max_hp=60, hp=40
    )
    p1 = PlayerState(active=pikachu, points=1)
    p2 = PlayerState(active=None)
    game = GameState(
        player1=p1, player2=p2,
        turn=1, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False
    )
    
    score = evaluate_state(game)
    print(f"Evaluation score: {score}")
    assert isinstance(score, int) or isinstance(score, float)
    print("✅ Evaluation returns a number")

def test_evaluation_point_advantage():
    """Test that points are weighted heavily."""
    # Player has points advantage
    p1_advantage = PlayerState(points=2, active=CATERPIE)
    p2_advantage = PlayerState(points=0, active=CATERPIE)
    game_advantage = GameState(
        player1=p1_advantage, player2=p2_advantage,
        turn=1, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False
    )
    
    # Player has point disadvantage
    p1_disadvantage = PlayerState(points=0, active=CATERPIE)
    p2_disadvantage = PlayerState(points=2, active=CATERPIE)
    game_disadvantage = GameState(
        player1=p1_disadvantage, player2=p2_disadvantage,
        turn=1, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False
    )
    
    score_advantage = evaluate_state(game_advantage)
    score_disadvantage = evaluate_state(game_disadvantage)
    
    print(f"Score with advantage: {score_advantage}")
    print(f"Score with disadvantage: {score_disadvantage}")
    assert score_advantage > score_disadvantage
    print("✅ Points advantage correctly evaluated")

def test_evaluation_evolution_bonus():
    """Test that evolved Pokemon get bonus."""
    # Basic Pokemon
    basic = Pokemon(
        name="Pikachu",
        card_type="pokemon",
        typing="Electric",
        max_hp=60, hp=40,
        stage="basic"
    )
    # Stage 1 Pokemon
    stage1 = Pokemon(
        name="Raichu",
        card_type="pokemon",
        typing="Electric",
        max_hp=90, hp=50,
        stage="stage1"
    )
    
    p1_basic = PlayerState(active=basic)
    p1_stage1 = PlayerState(active=stage1)
    p2 = PlayerState(active=None)
    
    game_basic = GameState(
        player1=p1_basic, player2=p2,
        turn=1, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False
    )
    
    game_stage1 = GameState(
        player1=p1_stage1, player2=p2,
        turn=1, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False
    )
    
    score_basic = evaluate_state(game_basic)
    score_stage1 = evaluate_state(game_stage1)
    
    print(f"Score with basic: {score_basic}")
    print(f"Score with stage1: {score_stage1}")
    assert score_stage1 > score_basic
    print("✅ Evolution bonus works")

if __name__ == "__main__":
    print("=" * 50)
    print("TESTING EVALUATOR")
    print("=" * 50)
    print()
    
    test_evaluation_basic()
    test_evaluation_point_advantage()
    test_evaluation_evolution_bonus()
    
    print("=" * 50)
    print("✅ All tests passed!")