"""Tests for ability mechanics."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.card import Pokemon
from src.models.ability import Ability
from src.models.effect import Effect
from src.models.game_state import PlayerState, GameState
from src.rules.actions import generate_actions, apply_action, start_turn
from src.cards.pokemon.butterfree import BUTTERFREE

def test_ability_action_generation():
    """Test that abilities appear in actions."""
    # Setup a Pokemon with an ability
    ability = Ability(
        name="Test Ability",
        ability_type="once_per_turn",
        req_active=True,
        effect=Effect(
            effect_type="heal",
            amount=30,
            target="active",
            target_condition="healable"
        )
    )
    
    pikachu = Pokemon(
        name="Pikachu",
        card_type="pokemon",
        typing="Electric",
        max_hp=60, hp=30,  # Damaged so ability can be used
        ability=ability,
        attacks=[]
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
    print(f"Actions: {actions}")
    
    ability_actions = [a for a in actions if a.startswith("USE_ABILITY_")]
    assert len(ability_actions) > 0
    print("✅ Ability appears in actions")

def test_ability_once_per_turn():
    """Test that once-per-turn ability can't be used twice."""
    ability = Ability(
        name="Test Ability",
        ability_type="once_per_turn",
        req_active=True,
        used_this_turn=False,
        effect=Effect(
            effect_type="heal",
            amount=30,
            target="active",
            target_condition="healable"
        )
    )
    
    pikachu = Pokemon(
        name="Pikachu",
        card_type="pokemon",
        typing="Electric",
        max_hp=60, hp=30,
        ability=ability,
        attacks=[]
    )
    
    player = PlayerState(active=pikachu)
    game = GameState(
        player1=player, player2=PlayerState(),
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False
    )
    
    # First use should be available
    actions1 = generate_actions(game)
    ability_actions1 = [a for a in actions1 if a.startswith("USE_ABILITY_")]
    print(f"First turn actions: {actions1}")
    assert len(ability_actions1) == 1
    
    # Use the ability
    game = apply_action(game, ability_actions1[0])
    
    # Second use should NOT be available
    actions2 = generate_actions(game)
    ability_actions2 = [a for a in actions2 if a.startswith("USE_ABILITY_")]
    print(f"Second turn actions: {actions2}")
    assert len(ability_actions2) == 0
    print("✅ Once-per-turn ability limited to one use")

def test_ability_resets_at_turn_start():
    """Test that abilities reset at start of turn."""
    ability = Ability(
        name="Test Ability",
        ability_type="once_per_turn",
        req_active=True,
        used_this_turn=True,  # Already used
        effect=Effect(
            effect_type="heal",
            amount=30,
            target="active",
            target_condition="healable"
        )
    )
    
    pikachu = Pokemon(
        name="Pikachu",
        card_type="pokemon",
        typing="Electric",
        max_hp=60, hp=30,
        ability=ability,
        attacks=[]
    )
    
    player = PlayerState(active=pikachu, energy_types=["Fire"])
    game = GameState(
        player1=player, player2=PlayerState(),
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False
    )
    
    # Ability should not be available (already used)
    actions_before = generate_actions(game)
    ability_before = [a for a in actions_before if a.startswith("USE_ABILITY_")]
    print(f"Before start_turn: {ability_before}")
    assert len(ability_before) == 0
    
    # Start turn resets ability
    game = start_turn(game)
    
    # Ability should be available again
    actions_after = generate_actions(game)
    ability_after = [a for a in actions_after if a.startswith("USE_ABILITY_")]
    print(f"After start_turn: {ability_after}")
    assert len(ability_after) > 0
    print("✅ Abilities reset at start of turn")

def test_butterfree_ability_heal():
    """Test Butterfree's ability heals all Pokemon."""
    # Create Butterfree with ability
    butterfree = BUTTERFREE
    
    # Setup: Butterfree active, damaged bench Pokemon
    butterfree.hp = 100  # Damaged (max 120)
    
    bench_pokemon = Pokemon(
        name="Pikachu",
        card_type="pokemon",
        typing="Electric",
        max_hp=60, hp=40  # Damaged
    )
    
    player = PlayerState(active=butterfree, bench=[bench_pokemon])
    game = GameState(
        player1=player, player2=PlayerState(),
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False
    )
    
    print(f"Butterfree HP before: {game.player1.active.hp}")
    print(f"Bench HP before: {game.player1.bench[0].hp}")
    
    # Find ability action
    actions = generate_actions(game)
    ability_actions = [a for a in actions if a.startswith("USE_ABILITY_")]
    print(actions)
    print(f"Ability actions: {ability_actions}")
    
    # Use ability
    new_game = apply_action(game, ability_actions[0])
    
    print(f"Butterfree HP after: {new_game.player1.active.hp}")
    print(f"Bench HP after: {new_game.player1.bench[0].hp}")
    
    # Should heal 20 to both
    assert new_game.player1.active.hp == 120  # Capped at max
    assert new_game.player1.bench[0].hp == 60  # Capped at max
    print("✅ Butterfree ability heals all Pokemon")

def test_ability_target_conditions():
    """Test that abilities respect target conditions."""
    ability = Ability(
        name="Test Heal",
        ability_type="once_per_turn",
        req_active=True,
        effect=Effect(
            effect_type="heal",
            amount=30,
            target="any",
            target_condition="typing",
            target_condition_instance="Grass"
        )
    )
    
    # Setup: Active is Grass (healable), Bench is Electric (not healable)
    active = Pokemon(
        name="Bulbasaur",
        card_type="pokemon",
        typing="Grass",
        max_hp=70, hp=40,
        ability=ability,
        attacks=[]
    )
    bench = Pokemon(
        name="Pikachu",
        card_type="pokemon",
        typing="Electric",
        max_hp=60, hp=30,
        attacks=[]
    )
    
    player = PlayerState(active=active, bench=[bench])
    game = GameState(
        player1=player, player2=PlayerState(),
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False
    )
    
    actions = generate_actions(game)
    print(f"Actions: {actions}")
    
    # Should only generate action for Grass Pokemon (active)
    grass_actions = [a for a in actions if "USE_ABILITY_ACTIVE" in a]
    bench_actions = [a for a in actions if "USE_ABILITY_0" in a]
    
    assert len(grass_actions) == 1
    assert len(bench_actions) == 0
    print("✅ Ability respects target conditions")

if __name__ == "__main__":
    print("=" * 50)
    print("TESTING ABILITIES")
    print("=" * 50)
    print()
    
    test_ability_action_generation()
    test_ability_once_per_turn()
    test_ability_resets_at_turn_start()
    test_butterfree_ability_heal()
    test_ability_target_conditions()
    
    print("=" * 50)
    print("✅ All tests passed!")