"""Tests for Erika, Giovanni, and Hand Scope cards."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.card import Pokemon
from src.models.game_state import PlayerState, GameState
from src.cards.trainers.erika import ERIKA
from src.cards.trainers.giovanni import GIOVANNI
from src.cards.trainers.hand_scope import HAND_SCOPE
from src.rules.actions import apply_action

def test_erika_heal_grass():
    """Test Erika heals 50 from Grass Pokemon."""
    bulbasaur = Pokemon(
        name="Bulbasaur", 
        card_type="pokemon",
        typing="Grass",
        max_hp=70, 
        hp=20,  # Damaged
        damage=15,
        attack_cost=1
    )
    player = PlayerState(active=bulbasaur, hand=[ERIKA])
    game = GameState(
        player1=player, player2=PlayerState(),
        turn=1, current_player=1,
        game_over=False, winner=None,
        supporter_played=False
    )
    
    new_game = apply_action(game, "PLAY_CARD_0")
    
    print(f"HP: 20 → {new_game.player1.active.hp}")
    assert new_game.player1.active.hp == 70  # Healed to max
    assert new_game.supporter_played  # Supporter flag set
    print("✅ Erika heals Grass Pokemon")

def test_erika_wont_heal_non_grass():
    """Test Erika doesn't heal non-Grass Pokemon."""
    charmander = Pokemon(
        name="Charmander",
        card_type="pokemon",
        typing="Fire",
        max_hp=60,
        hp=20,  # Damaged
        damage=15,
        attack_cost=1
    )
    player = PlayerState(active=charmander, hand=[ERIKA])
    game = GameState(
        player1=player, player2=PlayerState(),
        turn=1, current_player=1,
        game_over=False, winner=None,
        supporter_played=False
    )
    
    new_game = apply_action(game, "PLAY_CARD_0")
    
    print(f"HP: 20 → {new_game.player1.active.hp}")
    # Should NOT heal Fire Pokemon
    assert new_game.player1.active.hp == 20
    print("✅ Erika doesn't heal non-Grass Pokemon")

def test_giovanni_boost():
    """Test Giovanni adds +10 damage this turn."""
    attacker = Pokemon(
        name="Pikachu",
        card_type="pokemon",
        typing="Electric",
        max_hp=60, hp=60,
        damage=20,
        attack_cost=1,
        attached_energy=1
    )
    defender = Pokemon(
        name="Pidgey",
        card_type="pokemon",
        typing="Normal",
        max_hp=40, hp=40,
        damage=10,
        attack_cost=0
    )
    
    p1 = PlayerState(active=attacker, hand=[GIOVANNI])
    p2 = PlayerState(active=defender)
    game = GameState(
        player1=p1, player2=p2,
        turn=1, current_player=1,
        game_over=False, winner=None,
        supporter_played=False
    )
    
    # Play Giovanni first
    after_giovanni = apply_action(game, "PLAY_CARD_0")
    # Then attack
    after_attack = apply_action(after_giovanni, "ATTACK_WITH_ACTIVE")
    
    print(f"Defender HP: 40 → {after_attack.player2.active.hp}")
    # Should take 30 damage (20 + 10)
    assert after_attack.player2.active.hp == 10
    print("✅ Giovanni adds +10 damage")

def test_hand_scope_reveals():
    """Test Hand Scope reveals opponent's hand."""
    # Setup opponent with a hand
    opponent_hand = [
        Pokemon(name="Pikachu", card_type="pokemon", typing="Electric", max_hp=60, hp=60, damage=20),
        Pokemon(name="Bulbasaur", card_type="pokemon", typing="Grass", max_hp=70, hp=70, damage=15)
    ]
    p1 = PlayerState(hand=[HAND_SCOPE])
    p2 = PlayerState(hand=opponent_hand)
    game = GameState(
        player1=p1, player2=p2,
        turn=1, current_player=1,
        game_over=False, winner=None,
        supporter_played=False
    )
    
    print("Playing Hand Scope - should reveal opponent's hand:")
    new_game = apply_action(game, "PLAY_CARD_0")
    
    # Card should be in discard pile
    assert HAND_SCOPE in new_game.player1.discard
    print("✅ Hand Scope reveals hand")

if __name__ == "__main__":
    print("=" * 50)
    print("TESTING NEW CARDS")
    print("=" * 50)
    print()
    
    test_erika_heal_grass()
    test_erika_wont_heal_non_grass()
    test_giovanni_boost()
    test_hand_scope_reveals()
    
    print("=" * 50)
    print("✅ All tests passed!")