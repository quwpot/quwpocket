"""Tests for evolution timing."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.card import Pokemon
from src.models.game_state import PlayerState, GameState
from src.rules.actions import generate_actions, apply_action, start_turn

def test_cannot_evolve_same_turn():
    """Test that Pokemon can't evolve on the turn it was played."""
    pikachu = Pokemon(
        name="Pikachu",
        card_type="pokemon",
        typing="Electric",
        max_hp=60, hp=60,
        damage=20,
        attack_cost=1,
        retreat_cost=1,
        stage="basic",
        turns_in_play=0  # Just played
    )
    raichu = Pokemon(
        name="Raichu",
        card_type="pokemon",
        typing="Electric",
        max_hp=90, hp=90,
        damage=40,
        attack_cost=2,
        stage="stage1",
        evolves_from="Pikachu"
    )
    player = PlayerState(active=pikachu, hand=[raichu])
    game = GameState(
        player1=player, player2=PlayerState(),
        turn=1, current_player=1,
        game_over=False, winner=None,
        supporter_played=False
    )
    
    actions = generate_actions(game)
    print(f"Actions: {actions}")
    
    # Should NOT have evolution action (turns_in_play=0)
    evolution_actions = [a for a in actions if a.startswith("PLAY_CARD_ACTIVE_")]
    assert len(evolution_actions) == 0
    print("✅ Cannot evolve same turn")

def test_can_evolve_next_turn():
    """Test that Pokemon can evolve after 1 full turn."""
    pikachu = Pokemon(
        name="Pikachu",
        card_type="pokemon",
        typing="Electric",
        max_hp=60, hp=60,
        damage=20,
        attack_cost=1,
        stage="basic",
        turns_in_play=1  # Been in play for 1 turn
    )
    raichu = Pokemon(
        name="Raichu",
        card_type="pokemon",
        typing="Electric",
        max_hp=90, hp=90,
        damage=40,
        attack_cost=2,
        stage="stage1",
        evolves_from="Pikachu"
    )
    player = PlayerState(active=pikachu, hand=[raichu])
    game = GameState(
        player1=player, player2=PlayerState(),
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False
    )
    
    actions = generate_actions(game)
    print(f"Actions: {actions}")
    
    # Should have evolution action
    evolution_actions = [a for a in actions if a.startswith("PLAY_CARD_ACTIVE_")]
    assert len(evolution_actions) > 0
    print("✅ Can evolve next turn")

def test_turns_in_play_increments():
    """Test that turns_in_play increments at start of turn."""
    pikachu = Pokemon(
        name="Pikachu",
        card_type="pokemon",
        typing="Electric",
        max_hp=60, hp=60,
        damage=20,
        attack_cost=1,
        stage="basic",
        turns_in_play=0
    )
    player = PlayerState(active=pikachu)
    game = GameState(
        player1=player, player2=PlayerState(),
        turn=1, current_player=1,
        game_over=False, winner=None,
        supporter_played=False
    )
    
    print(f"Before: {game.player1.active.turns_in_play}")
    game = start_turn(game)
    print(f"After: {game.player1.active.turns_in_play}")
    
    assert game.player1.active.turns_in_play == 1
    print("✅ turns_in_play increments")

if __name__ == "__main__":
    print("=" * 50)
    print("TESTING EVOLUTION TIMING")
    print("=" * 50)
    print()
    
    test_cannot_evolve_same_turn()
    test_can_evolve_next_turn()
    test_turns_in_play_increments()
    
    print("=" * 50)
    print("✅ All tests passed!")