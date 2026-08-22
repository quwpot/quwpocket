"""Tests for Fossil mechanics."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.card import Fossil
from src.models.game_state import PlayerState, GameState
from src.rules.actions import generate_actions, apply_action

def test_fossil_play_to_bench():
    """Test playing Fossil to bench."""
    fossil = Fossil(
        name="Mysterious Fossil",
        card_type="fossil",
        max_hp=40,
        hp=40,
        typing="Colorless"
    )
    
    player = PlayerState(hand=[fossil], bench=[])
    game = GameState(
        player1=player, player2=PlayerState(),
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False
    )
    
    actions = generate_actions(game)
    print(f"Actions with Fossil in hand: {actions}")
    
    # Should be able to play Fossil to bench
    assert any(a.startswith("PLAY_CARD_") for a in actions)
    
    new_game = apply_action(game, "PLAY_CARD_0", debug=True)
    print(f"Bench size: {len(new_game.player1.bench)}")
    print(f"Bench Pokemon: {new_game.player1.bench[0].name}")
    
    assert len(new_game.player1.bench) == 1
    assert new_game.player1.bench[0].name == "Mysterious Fossil"
    print("✅ Fossil played to bench")

def test_fossil_cannot_retreat():
    """Test that Fossil cannot retreat."""
    fossil = Fossil(
        name="Mysterious Fossil",
        card_type="fossil",
        max_hp=40,
        hp=40,
        typing="Colorless",
    )
    
    player = PlayerState(active=fossil, bench=[])
    game = GameState(
        player1=player, player2=PlayerState(),
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False
    )
    
    actions = generate_actions(game)
    print(f"Actions with Fossil active: {actions}")
    
    # Should NOT have retreat action
    retreat_actions = [a for a in actions if a.startswith("RETREAT_")]
    assert len(retreat_actions) == 0
    print("✅ Fossil cannot retreat")

def test_discard_fossil_bench():
    """Test discarding Fossil from bench."""
    fossil = Fossil(
        name="Mysterious Fossil",
        card_type="fossil",
        max_hp=40,
        hp=40,
        typing="Colorless",
    )
    
    player = PlayerState(bench=[fossil])
    game = GameState(
        player1=player, player2=PlayerState(),
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False
    )
    
    actions = generate_actions(game)
    print(f"Actions with Fossil on bench: {actions}")
    
    # Should have discard action
    discard_actions = [a for a in actions if a.startswith("DISCARD_FOSSIL_")]
    assert len(discard_actions) == 1
    
    new_game = apply_action(game, discard_actions[0])
    print(f"Bench size after discard: {len(new_game.player1.bench)}")
    
    assert len(new_game.player1.bench) == 0
    print("✅ Fossil discarded from bench")

if __name__ == "__main__":
    print("=" * 50)
    print("TESTING FOSSILS")
    print("=" * 50)
    print()
    
    test_fossil_play_to_bench()
    test_fossil_cannot_retreat()
    test_discard_fossil_bench()
    
    print("=" * 50)
    print("✅ All tests passed!")