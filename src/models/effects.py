from dataclasses import dataclass
from copy import deepcopy
from typing import Optional
from src.models.game_state import GameState
from src.models.card import Trainer

def apply_heal(state: GameState, effect: Effect, target: str) -> GameState:
    
    """
Generic heal effect.

1. Where should we heal?
2. How much should be healed?
    """

    nstate = deepcopy(state)
    player = nstate.player1 if nstate.current_player == 1 else nstate.player2

    if not effect.target == "all_own":

        if target == "ACTIVE":
            player.active.hp += effect.amount

            if player.active.hp > player.active.max_hp:
                player.active.hp = player.active.max_hp

        else:
            player.bench[int(target)].hp += effect.amount

            if player.bench[int(target)].hp > player.bench[int(target)].max_hp:
                player.bench[int(target)].hp = player.bench[int(target)].max_hp

    else:
        for card in [player.active] + player.bench:
            card.hp += effect.amount

            if card.hp > card.max_hp:
                card.hp = card.max_hp

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

def apply_attach_energy(state: GameState, effect: Effect, target: str) -> GameState:
    
    """
Generic energy attach effect.

1. Where should we attach?
2. How many should we attach?
3. What Type should be attached?
    """

    nstate = deepcopy(state)
    player = nstate.player1 if nstate.current_player == 1 else nstate.player2

    if target == "ACTIVE":
        for i in range(effect.amount):
            player.active.attached_energy.append(effect.instance)

    else:
        for i in range(effect.amount):
            player.bench[int(target)].attached_energy.append(effect.instance)
    
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

def apply_discard_energy(state: GameState, effect: Effect, target: str) -> GameState:

    """
Discards {amount} energy from a specified Pokemon.
    """

    nstate = deepcopy(state)
    player = nstate.player1 if nstate.current_player == 1 else nstate.player2

    if target == "active":
        if effect.target_condition == "typing":
            for i in range(effect.amount):
                player.active.attached_energy.remove(effect.target_condition_instance)

    return nstate

def apply_deck_to_hand(state: GameState, effect: Effect) -> GameState:

    """
Puts {amount} specific cards from deck into players' hand.
    """

    nstate = deepcopy(state)
    player = nstate.player1 if nstate.current_player == 1 else nstate.player2

    choices = []

    if effect.target_condition == "typing":
        for card in player.deck:
            if card.typing:
                if card.typing == effect.target_condition_instance:
                    choices.append(card)

    elif effect.target_condition == "stage":
        for card in player.deck:
            if card.stage:
                if card.stage == effect.target_condition_instance:
                    choices.append(card)

    for i in range(effect.amount):
        if not choices:
            break
        player.hand.append(choices.pop(randrange(len(choices) + 1)))

    return nstate