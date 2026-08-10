"""Simple tests for the card models."""

import sys
import os
# Add parent directory to path so we can import src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.card import Pokemon, Trainer
from src.models.game_state import PlayerState, GameState, create_initial_state

def test_card_creation():
    """Test that cards are created correctly."""
    # Create a basic card
    basic_card = Card(name="Basic Card", card_type="test")
    print(f"Basic card: {basic_card}")
    print(f"  - Name: {basic_card.name}")
    print(f"  - Type: {basic_card.card_type}")
    print()

def test_pokemon_creation():
    """Test Pokemon creation and __repr__."""
    # Create a non-ex Pokemon with no energy
    pikachu = Pokemon(name="Pikachu", card_type="pokemon", hp=60, damage=20)
    print(f"Pikachu: {pikachu}")
    
    # Create an ex Pokemon with energy
    charizard_ex = Pokemon(
        name="Charizard", 
        card_type="pokemon", 
        hp=180, 
        damage=150, 
        is_ex=True, 
        attached_energy=2
    )
    print(f"Charizard ex: {charizard_ex}")
    
    # Create a Pokemon with energy but check the repr shows it correctly
    raichu = Pokemon(name="Raichu", card_type="pokemon", hp=90, damage=40, attached_energy=1)
    print(f"Raichu with energy: {raichu}")
    print()

def test_trainer_creation():
    """Test Trainer creation."""
    # Create an Item
    potion = Trainer(
        name="Potion",
        card_type="trainer",
        is_supporter=False,
        description="Heal 30 damage from one Pokemon"
    )
    print(f"Item card: {potion}")
    
    # Create a Supporter
    professor = Trainer(
        name="Professor's Research",
        card_type="trainer",
        is_supporter=True,
        description="Discard your hand and draw 7 cards"
    )
    print(f"Supporter card: {professor}")
    print()

def test_inheritance():
    """Test that inheritance works correctly."""
    pikachu = Pokemon(name="Pikachu", card_type="pokemon", hp=60, damage=20)
    
    # Check that Pokemon has Card's attributes
    print(f"Pikachu has name: {hasattr(pikachu, 'name')} - {pikachu.name}")
    print(f"Pikachu has card_type: {hasattr(pikachu, 'card_type')} - {pikachu.card_type}")
    print(f"Pikachu is a Card instance: {isinstance(pikachu, Card)}")
    print(f"Pikachu is a Pokemon instance: {isinstance(pikachu, Pokemon)}")
    print()

if __name__ == "__main__":
    print("=" * 50)
    print("TESTING CARD MODELS")
    print("=" * 50)
    print()
    
    test_card_creation()
    test_pokemon_creation()
    test_trainer_creation()
    test_inheritance()
    
    print("=" * 50)
    print("All tests completed!")