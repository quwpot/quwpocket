"""Tests for the new energy system."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.card import Pokemon
from src.models.game_state import create_initial_state, PlayerState, GameState
from src.rules.actions import apply_action, start_turn
from src.cards.pokemon.pikachu import PIKACHU

def test_energy_generation_types():
    """Test that energy generates from chosen types."""
    deck = [PIKACHU] * 20
    energy_types = ["Fire", "Water"]
    game = create_initial_state(deck, deck, energy_types)
    
    print(f"Player 1 energy types: {game.player1.energy_types}")
    print(f"Player 1 next energy: {game.player1.next_energy_type}")
    print(f"Player 1 current energy: {game.player1.current_energy_type}")
    
    assert game.player1.energy_types == ["Fire", "Water"]
    assert game.player1.next_energy_type in ["Fire", "Water"]
    print("✅ Energy types configured")

def test_energy_attachment_tracks_types():
    """Test that attached energy tracks specific types."""
    pikachu = Pokemon(
        name="Pikachu",
        card_type="pokemon",
        typing="Electric",
        max_hp=60, hp=60,
        damage=20, stage="Basic"
    )
    player = PlayerState(active=pikachu, energy_available=True, current_energy_type="Fire")
    game = GameState(
        player1=player, player2=PlayerState(),
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False
    )
    
    # Attach energy
    game = apply_action(game, "ATTACH_ENERGY_TO_SLOT_ACTIVE")
    
    print(f"Attached energy: {game.player1.active.attached_energy}")
    assert "Fire" in game.player1.active.attached_energy
    assert len(game.player1.active.attached_energy) == 1
    print("✅ Energy tracks specific types")

def test_multiple_energy_attachments():
    """Test attaching multiple energies of different types."""
    pikachu = Pokemon(
        name="Pikachu",
        card_type="pokemon",
        typing="Electric",
        max_hp=60, hp=60,
        damage=20,
        stage="Basic"
    )
    player = PlayerState(active=pikachu, energy_available=True, current_energy_type="Fire", energy_types=["Fire"])
    game = GameState(
        player1=player, player2=PlayerState(energy_types=["Fire"]),
        turn=2, current_player=1,
        game_over=False, winner=None,
        supporter_played=False,
        is_first_turn=False
    )
    
    # Attach Fire
    game = apply_action(game, "ATTACH_ENERGY_TO_SLOT_ACTIVE")
    
    # End turn, start new turn with Water
    game = apply_action(game, "END_TURN")
    game = apply_action(game, "END_TURN")  # Back to Player 1
    game.player1.current_energy_type = "Water"
    game.player1.energy_available = True
    
    # Attach Water
    game = apply_action(game, "ATTACH_ENERGY_TO_SLOT_ACTIVE")
    
    print(f"Attached energy: {game.player1.active.attached_energy}")
    assert "Fire" in game.player1.active.attached_energy
    assert "Water" in game.player1.active.attached_energy
    assert len(game.player1.active.attached_energy) == 2
    print("✅ Multiple energy types attach correctly")

if __name__ == "__main__":
    print("=" * 50)
    print("TESTING ENERGY SYSTEM")
    print("=" * 50)
    print()
    
    test_energy_generation_types()
    test_energy_attachment_tracks_types()
    test_multiple_energy_attachments()
    
    print("=" * 50)
    print("✅ All tests passed!")