"""Verify that playing a card removes it from hand."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.card import Pokemon
from src.models.game_state import PlayerState, GameState
from src.cards.trainers.potion import POTION
from src.rules.actions import apply_action, generate_actions

def test_hand_shrinks_after_play():
    """Play a trainer - hand must have one fewer card."""
    pikachu = Pokemon(
        name="Pikachu", card_type="pokemon", typing="Electric",
        max_hp=60, hp=60, attacks=[]
    )
    player = PlayerState(active=pikachu, hand=[POTION, POTION])
    game = GameState(
        player1=player, player2=PlayerState(),
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False,
        pending_promotion=False,
        pending_player=0
    )
    
    print(f"Hand before: {len(game.player1.hand)}")
    game = apply_action(game, "PLAY_CARD_ACTIVE_0")
    print(f"Hand after: {len(game.player1.hand)}")
    
    assert len(game.player1.hand) == 1
    print("✅ Hand shrinks correctly")

def test_no_repeat_same_card_forever():
    """Play the same card index twice in a row - hand must shrink each time."""
    pikachu = Pokemon(
        name="Pikachu", card_type="pokemon", typing="Electric",
        max_hp=60, hp=10, attacks=[]
    )
    player = PlayerState(active=pikachu, hand=[POTION, POTION, POTION])
    game = GameState(
        player1=player, player2=PlayerState(),
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False,
        pending_promotion=False,
        pending_player=0
    )
    
    for i in range(3):
        print(f"Before play {i+1}: hand size {len(game.player1.hand)}")
        actions = generate_actions(game)
        play_actions = [a for a in actions if a.startswith("PLAY_CARD_")]
        print(f"  Play actions: {play_actions}")
        game = apply_action(game, play_actions[0])
    
    print(f"Final hand size: {len(game.player1.hand)}")
    assert len(game.player1.hand) == 0
    print("✅ Multiple plays shrink hand each time")

if __name__ == "__main__":
    print("=" * 50)
    print("TESTING HAND SHRINKAGE")
    print("=" * 50)
    print()
    
    test_hand_shrinks_after_play()
    test_no_repeat_same_card_forever()
    
    print("=" * 50)
    print("✅ Test passed!")