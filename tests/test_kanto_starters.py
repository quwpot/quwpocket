"""Tests for Bulbasaur evolution line cards."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cards.pokemon.bulbasaur import BULBASAUR
from src.cards.pokemon.ivysaur import IVYSAUR
from src.cards.pokemon.venusaur import VENUSAUR
from src.models.game_state import PlayerState, GameState
from src.rules.actions import generate_actions, apply_action

def test_card_creation():
    """Test that cards are created correctly."""
    print(f"Bulbasaur: HP={BULBASAUR.hp}, stage={BULBASAUR.stage}")
    print(f"Ivysaur: HP={IVYSAUR.hp}, stage={IVYSAUR.stage}")
    print(f"Venusaur: HP={VENUSAUR.hp}, stage={VENUSAUR.stage}")
    
    assert BULBASAUR.name == "Bulbasaur"
    assert IVYSAUR.stage == "stage1"
    assert VENUSAUR.stage == "stage2"
    print("✅ Cards created correctly")

def test_attack_requirements():
    """Test that attacks have correct requirements."""
    attack = BULBASAUR.attacks[0]
    print(f"Bulbasaur attack: {attack.name}, cost: {attack.cost}")
    
    # Should have 2 energy requirements
    assert len(attack.cost) == 2
    assert attack.cost[0].energy_type == "Grass"
    assert attack.cost[1].energy_type == "Colorless"
    print("✅ Attack requirements correct")

if __name__ == "__main__":
    print("=" * 50)
    print("TESTING BULBASAUR EVOLUTION LINE")
    print("=" * 50)
    print()
    
    test_card_creation()
    test_attack_requirements()
    
    print("=" * 50)
    print("✅ All tests passed!")