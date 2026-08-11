from dataclasses import dataclass
from copy import deepcopy
from typing import Optional
from src.models.game_state import GameState
from src.models.card import Trainer

def apply_heal(state: GameState, card: Trainer) -> GameState:
    
    """
Generic heal effect.

1. Where should we heal?
2. How much should be healed?
    """

    nstate = deepcopy(state)
    player = nstate.player1 if nstate.current_player == 1 else nstate.player2

    if card.effect.target in ["active", "any"]:
        if card.effect.target_condition:
            if card.effect.target_condition == "typing":
                if card.effect.target_condition_instance == player.active.typing:
                    player.active.hp += card.effect.amount
        else:
            player.active.hp += card.effect.amount
    if player.active.hp > player.active.max_hp:
        player.active.hp = player.active.max_hp

    return nstate

def apply_draw(state: GameState, card: Trainer) -> GameState:
    
    """
Generic draw effect.

1. How many cards should get drawn
    """

    nstate = deepcopy(state)
    player = nstate.player1 if nstate.current_player == 1 else nstate.player2

    for i in range(card.effect.amount):
        player.hand.append(player.deck.pop())

    return nstate

def apply_attach_energy(state: GameState, card: Trainer) -> GameState:
    
    """
Generic energy attach effect.

1. Where should we attach?
2. How many should we attach?
3. What Type should be attached?
    """

    nstate = deepcopy(state)
    player = nstate.player1 if nstate.current_player == 1 else nstate.player2

    if card.effect.target in ["active", "any"]:
        player.active.attached_energy += card.effect.amount #no types for now
    
    return nstate

def apply_damage_boost(state: GameState, card: Trainer) -> GameState:

    """
Generic Damage Boost effect.

1. How much additional damage?
    """

    nstate = deepcopy(state)
    player = nstate.player1 if nstate.current_player == 1 else nstate.player2

    player.damage_boost += card.effect.amount

    return nstate

def apply_watch_opponent_hand_cards(state: GameState, card: Trainer) -> GameState:

    """
Reveals {amount} cards out of the opponents Hand.
    """

    #just watching, not modifying anything so no need for deepcopy()

    opponent = state.player1 if state.current_player == 2 else state.player2

    for i in range(min(card.effect.amount, len(opponent.hand))):
        print(opponent.hand[i])

    return state