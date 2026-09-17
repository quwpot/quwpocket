"""Tests for KO → promotion → turn end flow."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement
from src.models.game_state import PlayerState, GameState
from src.rules.actions import generate_actions, apply_action

def test_ko_flow_ends_turn():
    """Test that turn switches after promotion completes."""
    attacker = Pokemon(
        name="Pikachu",
        card_type="pokemon",
        typing="Electric",
        max_hp=60, hp=60,
        attacks=[Attack(
            name="Thunder Shock",
            damage=30,
            cost=[AttackRequirement("Colorless", 1)]
        )],
        attached_energy=["Electric"]
    )
    defender = Pokemon(
        name="Pichu",
        card_type="pokemon",
        typing="Electric",
        max_hp=30, hp=30
    )
    bench_pokemon = Pokemon(
        name="Raichu",
        card_type="pokemon",
        typing="Electric",
        max_hp=90, hp=90
    )
    
    p1 = PlayerState(active=attacker, energy_types=["Fire"])
    p2 = PlayerState(active=defender, bench=[bench_pokemon], energy_types=["Fire"])
    game = GameState(
        player1=p1, player2=p2,
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False,
        pending_promotion=False,
        pending_player=0
    )
    
    # Attack → KO → pending promotion
    game = apply_action(game, "ATTACK_0")
    
    print(f"After attack:")
    print(f"  current_player: {game.current_player}")
    print(f"  pending_promotion: {game.pending_promotion}")
    print(f"  pending_player: {game.pending_player}")
    
    assert game.pending_promotion is True
    assert game.pending_player == 2
    
    # Now promote
    game = apply_action(game, "PROMOTE_FROM_BENCH_0")
    
    print(f"\nAfter promotion:")
    print(f"  current_player: {game.current_player}")
    print(f"  turn: {game.turn}")
    print(f"  P2 active: {game.player2.active.name}")
    
    # Turn should have switched to P2 (opponent who promoted)
    assert game.current_player == 2
    assert game.player2.active.name == "Raichu"
    assert game.pending_promotion is False
    print("✅ Turn ended correctly after promotion")

if __name__ == "__main__":
    print("=" * 50)
    print("TESTING KO → PROMOTION → TURN END")
    print("=" * 50)
    print()
    
    test_ko_flow_ends_turn()
    
    print("=" * 50)
    print("✅ Test passed!")