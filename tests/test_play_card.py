"""Test playing cards."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.card import Pokemon
from src.models.game_state import PlayerState, GameState
from src.cards.trainers.potion import POTION
from src.rules.actions import generate_actions, apply_action

def test_play_potion():
    """Test playing Potion from hand."""
    pikachu = Pokemon(name="Pikachu", max_hp=60, hp=20, damage=20, attack_cost=1, card_type="pokemon")
    player = PlayerState(active=pikachu, hand=[POTION])
    game = GameState(
        player1=player, player2=PlayerState(),
        turn=1, current_player=1,
        game_over=False, winner=None,
        supporter_played=False
    )
    
    new_game = apply_action(game, "PLAY_CARD_0")
    
    print(f"HP: 20 → {new_game.player1.active.hp}")
    print(f"Hand: {len(new_game.player1.hand)} cards (should be 0)")
    print(f"Discard: {len(new_game.player1.discard)} cards (should be 1)")
    
    assert new_game.player1.active.hp == 40
    assert len(new_game.player1.hand) == 0
    assert len(new_game.player1.discard) == 1
    print("✅ Potion works!")

if __name__ == "__main__":
    test_play_potion()