"""Tests for special conditions, coin flips, and targeted effects."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement
from src.models.effect import Effect
from src.models.game_state import PlayerState, GameState
from src.rules.actions import generate_actions, apply_action, start_turn

def test_sleep_blocks_attack():
    """Test that asleep Pokemon cannot attack."""
    pikachu = Pokemon(
        name="Pikachu",
        card_type="pokemon",
        typing="Electric",
        max_hp=60, hp=60,
        special_conditions=2,  # Sleep bit set
        attacks=[
            Attack(
                name="Thunder Shock",
                damage=20,
                cost=[AttackRequirement("Colorless", 1)]
            )
        ],
        attached_energy=["Electric"]
    )
    
    player = PlayerState(active=pikachu)
    game = GameState(
        player1=player, player2=PlayerState(),
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False,
        pending_promotion=False,
        pending_player=0
    )
    
    actions = generate_actions(game)
    print(f"Actions with asleep Pokemon: {actions}")
    
    attack_actions = [a for a in actions if a.startswith("ATTACK_")]
    assert len(attack_actions) == 0
    print("✅ Asleep Pokemon cannot attack")

def test_sleep_blocks_retreat():
    """Test that asleep Pokemon cannot retreat."""
    pikachu = Pokemon(
        name="Pikachu",
        card_type="pokemon",
        typing="Electric",
        max_hp=60, hp=60,
        special_conditions=2,  # Sleep bit set
        retreat_cost=1,
        attached_energy=["Electric"]
    )
    bench_pokemon = Pokemon(
        name="Raichu",
        card_type="pokemon",
        typing="Electric",
        max_hp=90, hp=90
    )
    
    player = PlayerState(active=pikachu, bench=[bench_pokemon])
    game = GameState(
        player1=player, player2=PlayerState(),
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False,
        pending_promotion=False,
        pending_player=0
    )
    
    actions = generate_actions(game)
    print(f"Actions with asleep Pokemon: {actions}")
    
    retreat_actions = [a for a in actions if a.startswith("RETREAT_")]
    assert len(retreat_actions) == 0
    print("✅ Asleep Pokemon cannot retreat")

def test_poison_damage():
    """Test that poison deals damage at start of turn."""
    pikachu = Pokemon(
        name="Pikachu",
        card_type="pokemon",
        typing="Electric",
        max_hp=60, hp=60,
        special_conditions=1  # Poison bit set
    )
    opponent = Pokemon(
        name="Opponent",
        card_type="pokemon",
        typing="Colorless",
        max_hp=100, hp=100
    )
    
    player = PlayerState(active=pikachu, energy_types=["Fire"])
    p2 = PlayerState(active=opponent, energy_types=["Fire"])
    game = GameState(
        player1=player, player2=p2,
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False,
        pending_promotion=False,
        pending_player=0
    )
    
    print(f"HP before poison: {game.player1.active.hp}")
    game = start_turn(game)
    print(f"HP after poison: {game.player1.active.hp}")
    
    assert game.player1.active.hp == 50  # 60 - 10
    print("✅ Poison deals 10 damage")

def test_poison_knockout():
    """Test that poison can cause knockout."""
    pikachu = Pokemon(
        name="Pikachu",
        card_type="pokemon",
        typing="Electric",
        max_hp=10, hp=10,  # Low HP
        special_conditions=1  # Poison bit set
    )
    opponent = Pokemon(
        name="Opponent",
        card_type="pokemon",
        typing="Colorless",
        max_hp=100, hp=100
    )
    
    player = PlayerState(active=pikachu, energy_types=["Fire"])
    p2 = PlayerState(active=opponent, energy_types=["Fire"])
    game = GameState(
        player1=player, player2=p2,
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False,
        pending_promotion=False,
        pending_player=0
    )
    
    game = start_turn(game)
    print(f"Game over: {game.game_over}")
    print(f"Winner: {game.winner}")
    
    assert game.game_over is True
    assert game.winner == 2  # Opponent wins
    print("✅ Poison can cause knockout")

def test_evolution_removes_conditions():
    """Test that evolution removes special conditions."""
    pikachu = Pokemon(
        name="Pikachu",
        card_type="pokemon",
        typing="Electric",
        max_hp=60, hp=60,
        special_conditions=2,  # Sleep
        stage="basic"
    )
    raichu = Pokemon(
        name="Raichu",
        card_type="pokemon",
        typing="Electric",
        max_hp=90, hp=90,
        stage="stage1",
        evolves_from="Pikachu",
        attacks=[]
    )
    
    player = PlayerState(active=pikachu, hand=[raichu])
    game = GameState(
        player1=player, player2=PlayerState(),
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False,
        pending_promotion=False,
        pending_player=0
    )
    
    print(f"Special conditions before: {game.player1.active.special_conditions}")
    game = apply_action(game, "PLAY_CARD_ACTIVE_0")
    print(f"Special conditions after: {game.player1.active.special_conditions}")
    
    assert game.player1.active.special_conditions == 0
    print("✅ Evolution removes special conditions")

def test_retreat_removes_conditions():
    """Test that retreat removes special conditions."""
    pikachu = Pokemon(
        name="Pikachu",
        card_type="pokemon",
        typing="Electric",
        max_hp=60, hp=60,
        special_conditions=1,  # Poison
        retreat_cost=1,
        attached_energy=["Electric"]
    )
    raichu = Pokemon(
        name="Raichu",
        card_type="pokemon",
        typing="Electric",
        max_hp=90, hp=90
    )
    
    player = PlayerState(active=pikachu, bench=[raichu])
    game = GameState(
        player1=player, player2=PlayerState(),
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False,
        pending_promotion=False,
        pending_player=0
    )
    
    print(f"Special conditions before: {game.player1.active.special_conditions}")
    game = apply_action(game, "RETREAT_TO_SLOT_0")
    print(f"Special conditions after: {game.player1.active.special_conditions}")
    
    assert game.player1.active.special_conditions == 0
    print("✅ Retreat removes special conditions")

def test_coin_flip_attack():
    """Test coin flip attack effect."""
    attack = Attack(
        name="Multi-Strike",
        damage=0,  # Base damage 0, all from coin flips
        cost=[AttackRequirement("Colorless", 1)],
        effect=Effect(
            effect_type="coin_flip_bonus_damage",
            amount=2,  # Flip 2 coins
            instance=30  # 30 damage per heads
        ),
        needs_target=False
    )
    
    pikachu = Pokemon(
        name="Pikachu",
        card_type="pokemon",
        typing="Electric",
        max_hp=60, hp=60,
        attacks=[attack],
        attached_energy=["Electric"]
    )
    defender = Pokemon(
        name="Defender",
        card_type="pokemon",
        typing="Colorless",
        max_hp=100, hp=100
    )
    
    p1 = PlayerState(active=pikachu, energy_types=["Fire"])
    p2 = PlayerState(active=defender, energy_types=["Fire"])
    game = GameState(
        player1=p1, player2=p2,
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False,
        pending_promotion=False,
        pending_player=0
    )
    
    # Attack with coin flips
    game = apply_action(game, "ATTACK_0")
    print(f"Defender HP: {game.player2.active.hp}")
    
    assert game.player2.active.hp < 100
    print("✅ Coin flip attack works")

def test_switch_opponent_active():
    """Test switching opponent's active Pokemon."""
    # Create attack with switch effect
    attack = Attack(
        name="Gust",
        damage=20,
        cost=[AttackRequirement("Colorless", 1)],
        effect=Effect(
            effect_type="switch_opponent_active",
            target="opponent_bench_0"  # Switch with first bench
        ),
        needs_target=True
    )
    
    pidgeot = Pokemon(
        name="Pidgeot",
        card_type="pokemon",
        typing="Colorless",
        max_hp=80, hp=80,
        attacks=[attack],
        attached_energy=["Colorless"]
    )
    
    # Opponent has active and bench
    opponent_active = Pokemon(
        name="Pikachu",
        card_type="pokemon",
        typing="Electric",
        max_hp=60, hp=60
    )
    opponent_bench = Pokemon(
        name="Raichu",
        card_type="pokemon",
        typing="Electric",
        max_hp=90, hp=90
    )
    
    p1 = PlayerState(active=pidgeot, energy_types=["Fire"])
    p2 = PlayerState(active=opponent_active, bench=[opponent_bench], energy_types=["Fire"])
    game = GameState(
        player1=p1, player2=p2,
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False,
        pending_promotion=False,
        pending_player=0
    )
    
    print(f"Opponent active before: {game.player2.active.name}")
    print(f"Opponent bench before: {[p.name for p in game.player2.bench]}")
    
    # Attack with switch effect
    game = apply_action(game, "ATTACK_0_0")
    
    print(f"Opponent active after: {game.player2.active.name}")
    print(f"Opponent bench after: {[p.name for p in game.player2.bench]}")
    
    assert game.player2.active.name == "Raichu"
    assert game.player2.bench[0].name == "Pikachu"
    print("✅ Switch opponent active works")

def test_attach_energy_to_bench_effect():
    """Test attaching energy to bench Pokemon."""
    attack = Attack(
        name="Energy Transfer",
        damage=0,
        cost=[AttackRequirement("Grass", 1)],
        effect=Effect(
            effect_type="attach_energy",
            amount=1,
            instance="Grass",
            target="bench"
        ),
        needs_target=True
    )
    
    venusaur = Pokemon(
        name="Venusaur",
        card_type="pokemon",
        typing="Grass",
        max_hp=160, hp=160,
        attacks=[attack],
        attached_energy=["Grass"]
    )
    
    bench_pokemon = Pokemon(
        name="Bulbasaur",
        card_type="pokemon",
        typing="Grass",
        max_hp=70, hp=70
    )
    
    p1 = PlayerState(active=venusaur, bench=[bench_pokemon], energy_types=["Fire"])
    game = GameState(
        player1=p1, player2=PlayerState(active=venusaur, energy_types=["Fire"]),
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False,
        pending_promotion=False,
        pending_player=0
    )
    
    print(f"Bench energy before: {game.player1.bench[0].attached_energy}")
    game = apply_action(game, "ATTACK_0_0")
    print(f"Bench energy after: {game.player1.bench[0].attached_energy}")
    
    assert "Grass" in game.player1.bench[0].attached_energy
    print("✅ Attach energy to bench works")

if __name__ == "__main__":
    print("=" * 50)
    print("TESTING NEW MECHANICS")
    print("=" * 50)
    print()
    
    test_sleep_blocks_attack()
    test_sleep_blocks_retreat()
    test_poison_damage()
    test_poison_knockout()
    test_evolution_removes_conditions()
    test_retreat_removes_conditions()
    test_coin_flip_attack()
    test_switch_opponent_active()
    test_attach_energy_to_bench_effect()
    
    print("=" * 50)
    print("✅ All tests passed!")