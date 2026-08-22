"""Tests for promotion mechanics."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.card import Pokemon
from src.models.game_state import PlayerState, GameState
from src.rules.actions import generate_actions, apply_action

def test_promotion_needed_after_knockout():
    """Test that promotion is required after knockout."""
    # Setup: Attacker (Pikachu) vs Defender (Pichu with 10 HP)
    pikachu = Pokemon(
        name="Pikachu",
        card_type="pokemon",
        typing="Electric",
        max_hp=60, hp=40,
        attack_cost=1,
        attached_energy=["Electric"]
    )
    pichu = Pokemon(
        name="Pichu",
        card_type="pokemon",
        typing="Electric",
        max_hp=30, hp=10,  # Low HP
        attack_cost=1
    )
    bench_pokemon = Pokemon(
        name="Raichu",
        card_type="pokemon",
        typing="Electric",
        max_hp=90, hp=50,
        attack_cost=2
    )
    
    p1 = PlayerState(active=pikachu)
    p2 = PlayerState(active=pichu, bench=[bench_pokemon])
    game = GameState(
        player1=p1, player2=p2,
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False,
        pending_promotion=False,
        pending_player=0
    )
    
    # Attack
    game = apply_action(game, "ATTACK_0")
    
    print(f"Pending promotion: {game.pending_promotion}")
    print(f"Pending player: {game.pending_player}")
    print(f"Active P2: {game.player2.active}")
    
    assert game.pending_promotion is True
    assert game.pending_player == 2
    assert game.player2.active is None
    print("✅ Promotion needed after knockout")

def test_only_promotion_actions_available():
    """Test that only promotion actions are available when pending."""
    bench_pokemon = Pokemon(
        name="Raichu",
        card_type="pokemon",
        typing="Electric",
        max_hp=90, hp=90,
        damage=40,
        attack_cost=2
    )
    
    p2 = PlayerState(bench=[bench_pokemon])
    game = GameState(
        player1=PlayerState(), player2=p2,
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False,
        pending_promotion=True,
        pending_player=2
    )
    
    actions = generate_actions(game)
    print(f"Actions when pending promotion: {actions}")
    
    # Should only have promotion actions
    promotion_actions = [a for a in actions if a.startswith("PROMOTE_FROM_BENCH_")]
    other_actions = [a for a in actions if not a.startswith("PROMOTE_FROM_BENCH_")]
    
    assert len(promotion_actions) == 1
    assert len(other_actions) == 0
    print("✅ Only promotion actions available")

def test_promotion_execution():
    """Test that promotion moves bench Pokemon to active."""
    bench_pokemon = Pokemon(
        name="Raichu",
        card_type="pokemon",
        typing="Electric",
        max_hp=90, hp=90,
        damage=40,
        attack_cost=2
    )
    
    p2 = PlayerState(bench=[bench_pokemon])
    game = GameState(
        player1=PlayerState(), player2=p2,
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False,
        pending_promotion=True,
        pending_player=2
    )
    
    print(f"Before promotion - Bench: {[p.name for p in game.player2.bench]}")
    print(f"Before promotion - Active: {game.player2.active}")
    
    game = apply_action(game, "PROMOTE_FROM_BENCH_0")
    
    print(f"After promotion - Bench: {[p.name for p in game.player2.bench]}")
    print(f"After promotion - Active: {game.player2.active.name}")
    
    assert game.player2.active.name == "Raichu"
    assert len(game.player2.bench) == 0
    assert game.pending_promotion is False
    print("✅ Promotion executed correctly")

def test_loss_when_no_bench():
    """Test that player loses when no bench Pokemon."""
    pikachu = Pokemon(
        name="Pikachu",
        card_type="pokemon",
        typing="Electric",
        max_hp=60, hp=60,
        damage=20,
        attack_cost=1,
        attached_energy=["Electric"]
    )
    pichu = Pokemon(
        name="Pichu",
        card_type="pokemon",
        typing="Electric",
        max_hp=30, hp=10,
        damage=10,
        attack_cost=1
    )
    
    p1 = PlayerState(active=pikachu)
    p2 = PlayerState(active=pichu, bench=[])  # No bench!
    game = GameState(
        player1=p1, player2=p2,
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False,
        pending_promotion=False,
        pending_player=0
    )
    
    # Attack - should cause game over
    game = apply_action(game, "ATTACK_0")
    
    print(f"Game over: {game.game_over}")
    print(f"Winner: {game.winner}")
    
    assert game.game_over is True
    assert game.winner == 1
    print("✅ Loss when no bench Pokemon")

if __name__ == "__main__":
    print("=" * 50)
    print("TESTING PROMOTION MECHANICS")
    print("=" * 50)
    print()
    
    test_promotion_needed_after_knockout()
    test_only_promotion_actions_available()
    test_promotion_execution()
    test_loss_when_no_bench()
    
    print("=" * 50)
    print("✅ All tests passed!")