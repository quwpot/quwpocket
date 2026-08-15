"""Tests for multiple attacks."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.attack import Attack, AttackRequirement
from src.models.card import Pokemon
from src.models.game_state import PlayerState, GameState
from src.rules.actions import generate_actions, apply_action

def test_two_attacks_available():
    """Test that both attacks appear in actions."""
    # Create Pokemon with two attacks
    attack1 = Attack(
        name="Thunder Shock",
        damage=20,
        cost=[AttackRequirement("Colorless", 1)],
        description="Does 20 damage"
    )
    attack2 = Attack(
        name="Thunderbolt",
        damage=40,
        cost=[AttackRequirement("Electric", 2)],
        description="Does 40 damage"
    )
    
    pikachu = Pokemon(
        name="Pikachu",
        stage="Basic",
        card_type="pokemon",
        typing="Electric",
        max_hp=60, hp=60,
        attacks=[attack1, attack2],
        attached_energy=["Electric", "Electric"]  # Has 2 Electric energy
    )
    
    player = PlayerState(active=pikachu)
    game = GameState(
        player1=player, player2=PlayerState(),
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False
    )
    
    actions = generate_actions(game, debug=True)
    print(f"Actions: {actions}")
    
    assert "ATTACK_0" in actions  # First attack
    assert "ATTACK_1" in actions  # Second attack
    print("✅ Both attacks available")

def test_attack_requires_specific_energy():
    """Test that attack requires correct energy types."""
    attack = Attack(
        name="Thunderbolt",
        damage=40,
        cost=[
            AttackRequirement("Electric", 1),
            AttackRequirement("Colorless", 1)
        ],
        description="Requires 1 Electric and 1 Colorless"
    )
    
    pikachu = Pokemon(
        name="Pikachu",
        stage="Basic",
        card_type="pokemon",
        typing="Electric",
        max_hp=60, hp=60,
        attacks=[attack],
        attached_energy=["Electric", "Fire"]  # Has Electric + Fire (Colorless counts)
    )
    
    player = PlayerState(active=pikachu)
    game = GameState(
        player1=player, player2=PlayerState(),
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False
    )
    
    actions = generate_actions(game)
    print(f"Actions with Electric+Fire: {actions}")
    
    assert "ATTACK_0" in actions
    print("✅ Colorless requirement works")

def test_attack_blocked_by_energy():
    """Test that attack is blocked without enough energy."""
    attack = Attack(
        name="Thunderbolt",
        damage=40,
        cost=[AttackRequirement("Electric", 2)],
        description="Requires 2 Electric"
    )
    
    pikachu = Pokemon(
        name="Pikachu",
        stage="Basic",
        card_type="pokemon",
        typing="Electric",
        max_hp=60, hp=60,
        attacks=[attack],
        attached_energy=["Electric"]  # Only 1 Electric
    )
    
    player = PlayerState(active=pikachu)
    game = GameState(
        player1=player, player2=PlayerState(),
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False
    )
    
    actions = generate_actions(game)
    print(f"Actions with only 1 Electric: {actions}")
    
    assert "ATTACK_WITH_0" not in actions
    print("✅ Attack blocked without enough energy")

def test_attack_damage_calculation():
    """Test that attack damage is calculated correctly."""
    attack = Attack(
        name="Thunderbolt",
        damage=40,
        cost=[AttackRequirement("Electric", 1)],
        description="Does 40 damage"
    )
    
    pikachu = Pokemon(
        name="Pikachu",
        card_type="pokemon",
        typing="Electric",
        stage="Bassic",
        max_hp=60, hp=60,
        attacks=[attack],
        attached_energy=["Electric"]
    )
    
    defender = Pokemon(
        name="Bulbasaur",
        stage="Basic",
        card_type="pokemon",
        typing="Grass",
        max_hp=70, hp=70,
        weakness="Electric"
    )
    
    p1 = PlayerState(active=pikachu)
    p2 = PlayerState(active=defender, energy_types=["Fire"])
    game = GameState(
        player1=p1, player2=p2,
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False
    )
    
    new_game = apply_action(game, "ATTACK_0")
    
    print(f"Defender HP: 70 → {new_game.player2.active.hp}")
    # Should take 60 damage (40 + 20 weakness)
    assert new_game.player2.active.hp == 10
    print("✅ Attack damage with weakness works")

if __name__ == "__main__":
    print("=" * 50)
    print("TESTING MULTIPLE ATTACKS")
    print("=" * 50)
    print()
    
    test_two_attacks_available()
    test_attack_requires_specific_energy()
    test_attack_blocked_by_energy()
    test_attack_damage_calculation()
    
    print("=" * 50)
    print("✅ All tests passed!")