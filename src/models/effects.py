from dataclasses import dataclass
from copy import deepcopy
from typing import Optional
from random import choice
from src.models.game_state import GameState
from src.models.card import Trainer

def apply_heal(state: GameState, effect: Effect) -> GameState:
    
    """
Generic heal effect.

1. Where should we heal?
2. How much should be healed?
    """

    nstate = deepcopy(state)
    player = nstate.player1 if nstate.current_player == 1 else nstate.player2

    if not effect.target == "all_own":

        if effect.target in ["ACTIVE", "active"]:
            player.active.hp += effect.amount

            if player.active.hp > player.active.max_hp:
                player.active.hp = player.active.max_hp

        else:
            player.bench[int(effect.target)].hp += effect.amount

            if player.bench[int(effect.target)].hp > player.bench[int(effect.target)].max_hp:
                player.bench[int(effect.target)].hp = player.bench[int(effect.target)].max_hp

    else:
        for card in [player.active] + player.bench:
            card.hp += effect.amount

            if card.hp > card.max_hp:
                card.hp = card.max_hp

    return nstate

def apply_draw(state: GameState, effect: Effect) -> GameState:
    
    """
Generic draw effect.

1. How many cards should get drawn
    """

    nstate = deepcopy(state)
    player = nstate.player1 if nstate.current_player == 1 else nstate.player2

    for i in range(effect.amount):
        if not player.deck:      
            break
        player.hand.append(player.deck.pop())

    return nstate

def apply_attach_energy(state: GameState, effect: Effect) -> GameState:
    
    """
Generic energy attach effect.

1. Where should we attach?
2. How many should we attach?
3. What Type should be attached?
    """

    nstate = deepcopy(state)
    player = nstate.player1 if nstate.current_player == 1 else nstate.player2

    if effect.target == "ACTIVE":
        for i in range(effect.amount):
            player.active.attached_energy.append(effect.instance)

    else:
        for i in range(effect.amount):
            player.bench[int(effect.target)].attached_energy.append(effect.instance)
    
    return nstate

def apply_damage_boost(state: GameState, effect: Effect) -> GameState:

    """
Generic Damage Boost effect.

1. How much additional damage?
    """

    nstate = deepcopy(state)
    player = nstate.player1 if nstate.current_player == 1 else nstate.player2
    player.damage_boost += effect.amount
    return nstate

def apply_watch_opponent_hand_cards(state: GameState, effect: Effect) -> GameState:

    """
Reveals {amount} cards out of the opponents Hand.
    """

    #just watching, not modifying anything so no need for deepcopy()

    opponent = state.player1 if state.current_player == 2 else state.player2
    for i in range(min(effect.amount, len(opponent.hand))):
        print(opponent.hand[i])
    return state

def apply_discard_energy(state: GameState, effect: Effect) -> GameState:

    """
Discards {amount} energy from a specified Pokemon.
    """

    nstate = deepcopy(state)
    player = nstate.player1 if nstate.current_player == 1 else nstate.player2

    target = effect.target
    if target == "active":
        if effect.target_condition == "typing":
            for i in range(effect.amount):
                try:
                    player.active.attached_energy.remove(effect.target_condition_instance)
                except ValueError:
                    break
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

def apply_coin_flip_bonus_damage(state: GameState, effect: Effect, debug: bool = False) -> GameState:

    """
Amplifies the damage of an attack based on the amount of heads in {amount} coin flips.
    """

    nstate = deepcopy(state)
    opponent = nstate.player2 if nstate.current_player == 1 else nstate.player1

    heads = 0

    for i in range(effect.amount):
        if choice([True, False]):
            heads += 1

    if debug: print(f"{heads} heads out of {effect.amount} flips")

    opponent.active.hp -= (heads * effect.instance)

    return nstate

def apply_switch_opponent_active(state: GameState, effect: Effect) -> GameState:

    """
Switches the opponent's active Pokemon with a target Benched Pokemon.
    """

    nstate = deepcopy(state)
    opponent = nstate.player2 if nstate.current_player == 1 else nstate.player1

    temp = opponent.active

    opponent.active = opponent.bench.pop(int(effect.target))

    opponent.bench.insert(int(effect.target), temp)

    return nstate

def apply_special_condition(state: GameState, effect: Effect) -> GameState:

    """
Gives the target a designated special condition.
    """

    nstate = deepcopy(state)
    opponent = nstate.player2 if nstate.current_player == 1 else nstate.player1

    
    condition_dict = {
  "poison": 1,
  "sleep": 2
    }

    if effect.target == "opponent":
        opponent.active.special_conditions | (1 << condition_dict[effect.instance])

    return nstate