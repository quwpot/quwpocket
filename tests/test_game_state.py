"""Tests for game state models."""

import sys
import os
# Add parent directory to path so we can import src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.card import Pokemon, Trainer
from src.models.game_state import PlayerState, GameState, create_initial_state

def test_player_state_creation():
    """Test creating a PlayerState."""
    # Create a Pokemon for active
    pikachu = Pokemon(name="Pikachu", card_type="pokemon", hp=60, damage=20)
    
    # Create bench Pokemon
    bench = [
        Pokemon(name="Raichu", card_type="pokemon", hp=90, damage=40),
        Pokemon(name="Pichu", card_type="pokemon", hp=30, damage=10)
    ]
    
    # Create hand (some cards)
    hand = [
        Trainer(name="Potion", card_type="trainer", is_supporter=False, description="Heal 30"),
        Pokemon(name="Eevee", card_type="pokemon", hp=50, damage=15)
    ]
    
    # Create player state
    player = PlayerState(
        active=pikachu,
        bench=bench,
        hand=hand,
        deck=[],  # Empty deck for now
        points=0,
        energy_type="Fire",
        energy_available=False
    )
    
    print(f"Player state: {player}")
    print(f"  Active: {player.active}")
    print(f"  Bench size: {len(player.bench)}")
    print(f"  Hand size: {len(player.hand)}")
    
    # Test that fields exist and have correct types
    assert hasattr(player, 'active')
    assert hasattr(player, 'bench')
    assert hasattr(player, 'hand')
    assert hasattr(player, 'deck')
    assert hasattr(player, 'points')
    assert hasattr(player, 'energy_available')
    
    print("✅ PlayerState test passed!")
    print()

def test_game_state_creation():
    """Test creating a GameState."""
    # Create two player states
    player1 = PlayerState(
        active=None,
        bench=[],
        hand=[],
        deck=[],
        points=0,
        energy_type="Fire",
        energy_available=False
    )
    
    player2 = PlayerState(
        active=None,
        bench=[],
        hand=[],
        deck=[],
        energy_type="Fire",
        points=0,
        energy_available=False
    )
    
    # Create game state
    game = GameState(
        player1=player1,
        player2=player2,
        turn=1,
        current_player=1,
        game_over=False,
        winner=None,
        supporter_played=False
    )
    
    print(f"Game state: {game}")
    print(f"  Turn: {game.turn}")
    print(f"  Current player: {game.current_player}")
    print(f"  Game over: {game.game_over}")
    
    # Test helper function
    initial = create_initial_state()
    print(f"Initial state created: {initial}")
    print(f"  Player1 has {len(initial.player1.hand)} cards in hand")
    print(f"  Player2 has {len(initial.player2.hand)} cards in hand")
    
    print("✅ GameState test passed!")
    print()

def test_state_constraints():
    """Test that dataclass defaults work correctly."""
    # Create a PlayerState with minimal arguments
    player = PlayerState()  # Should use all defaults
    
    assert player.active is None
    assert player.bench == []
    assert player.hand == []
    assert player.deck == []
    assert player.points == 0
    assert player.energy_available == False
    
    print("✅ Default values test passed!")

if __name__ == "__main__":
    print("=" * 50)
    print("TESTING GAME STATE MODELS")
    print("=" * 50)
    print()
    
    test_player_state_creation()
    test_game_state_creation()
    test_state_constraints()
    
    print("=" * 50)
    print("✅ All tests passed!")