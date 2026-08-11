from copy import deepcopy
from src.models.game_state import GameState
from src.models.effects import *

def generate_actions(state: GameState) -> list[str]:

    """
Returns a list of all possible actions (draw card, attach energy, attack, ...) from a current GameState.

1. Checks whose turn it is
2. Grab the representative PlayerState
3. Check which actions are possible.

Actions:
    "END_TURN"                              - always possible.
    "ATTACH_ENERGY_TO_ACTIVE"               - possible if energy zone still contains energy (i.e. no energy was attached yet).
    "ATTACK_WITH_ACTIVE"                    - possible if active pokemon has fulfilled the energy requirement for its attack.
    "PLAY_CARD_N" (for each card in hand)   - possible if: card is pokemon and bench is not full OR card is Item OR card is Supporter and no supporter was played yet.
    """

    current_player = state.current_player
    player = state.player1 if current_player == 1 else state.player2    
    
    actions = ["END_TURN"]

    if player.active is not None:
        if player.active.attached_energy >= player.active.attack_cost:        
            actions.append("ATTACK_WITH_ACTIVE")
        
        if player.energy_available:
            actions.append("ATTACH_ENERGY_TO_ACTIVE")

    for i, card in enumerate(player.hand):
        if card.card_type == "Pokemon":
            if len(player.bench) != 3:
                actions.append(f"PLAY_CARD_{i}")
        
        elif card.card_type == "Trainer":
            if card.is_supporter:
                if not state.supporter_played:
                    actions.append(f"PLAY_CARD_{i}")

            else:
                actions.append(f"PLAY_CARD_{i}")

    return actions

def apply_action(state: GameState, action:str) -> GameState:

    """
Modifies a GameState depending on what action was selected.

Actions:
    "END_TURN"                  - switches to the other player. increments turn count by 1. resets the supporter_played flag.
    "ATTACH_ENERGY_TO_ACTIVE"   - increments energy counter of active pokemon by 1. Empties the energy zone so attaching happens only once per turn.
    "ATTACK_WITH_ACTIVE"        - decrease opponent's HP by the amount of damage the attack inflicts. check for knockout. end turn (see END_TURN).
    "PLAY_CARD_N"               - Apply effect, move to discard pile.
    """
    
    nstate = copy_state(state)

    current_player = nstate.current_player
    player = nstate.player1 if current_player == 1 else nstate.player2
    opponent = nstate.player1 if current_player == 2 else nstate.player2   

    if action == "END_TURN":
        player.damage_boost = 0
        nstate.current_player = (current_player % 2) + 1
        nstate.turn += 1
        nstate.supporter_played = False

    elif action == "ATTACH_ENERGY_TO_ACTIVE":
        player.active.attached_energy += 1
        player.energy_available = False

    elif action == "ATTACK_WITH_ACTIVE":
        opponent.active.hp -= (player.active.damage + player.damage_boost)

        if opponent.active.hp <= 0:
            if opponent.active.is_ex:
                player.points += 2
            else:
                player.points += 1
            
            opponent.discard.append(opponent.active)
            opponent.active = None
            
            if player.points >= 3:
                nstate.game_over = True
                nstate.winner = current_player

        player.damage_boost = 0        
        nstate.current_player = (current_player % 2) + 1
        nstate.turn += 1
        nstate.supporter_played = False

    elif action.startswith("PLAY_CARD_"):
        card_index = int(action.split("_")[-1])
        card = player.hand[card_index]
        print(f"{card.name} gets played.")
     
        if card.effect.effect_type == "heal":
            nstate = apply_heal(nstate, card)
        elif card.effect.effect_type == "draw":
            nstate = apply_draw(nstate, card)
        elif card.effect.effect_type == "attach_energy":
            nstate = apply_attach_energy(nstate, card)
        elif card.effect.effect_type == "damage_boost":
            nstate = apply_damage_boost(nstate, card)
        elif card.effect.effect_type == "watch_opponent_hand_cards":
            nstate = apply_watch_opponent_hand_cards(nstate, card)
        
        if card.is_supporter:
            nstate.supporter_played = True

        player = nstate.player1 if current_player == 1 else nstate.player2       

        player.discard.append(player.hand.pop(card_index))
        print(f"Card {card_index} gets removed from {player.hand}.")

    return nstate

def copy_state(state: GameState) -> GameState:

    """
Duplicate a GameState to modify it whilst not breaking search algorithms later.
    """

    return deepcopy(state)