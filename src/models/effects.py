from dataclasses import dataclass
from copy import deepcopy
from typing import Optional
from src.models.game_state import GameState

def apply_heal(state: GameState, target: str, amount: int) -> GameState:
    
    """
Generic heal effect.

1. Where should we heal?
2. How much should be healed?
    """

    nstate = deepcopy(state)
    player = nstate.player1 if nstate.current_player == 1 else nstate.player2

    if target in ["active", "any"]:
        player.active.hp += amount
        if player.active.hp > player.active.max_hp:
            player.active.hp = player.active.max_hp

    return nstate

def apply_draw(state: GameState, amount: int) -> GameState:
    
    """
Generic draw effect.

1. How many cards should get drawn
    """

    nstate = deepcopy(state)
    player = nstate.player1 if nstate.current_player == 1 else nstate.player2

    for i in range(amount):
        player.hand.append(player.deck.pop())

    return nstate

def apply_attach_energy(state: GameState, target: str, amount: int, energy_type: str) -> GameState:
    
    """
Generic energy attach effect.

1. Where should we attach?
2. How many should we attach?
3. What Type should be attached?
    """

    nstate = deepcopy(state)
    player = nstate.player1 if nstate.current_player == 1 else nstate.player2

    if target == "active":
        player.active.attached_energy += amount #no types for now
    
    return nstate