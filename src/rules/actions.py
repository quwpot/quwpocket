from copy import deepcopy

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
        actions.append("ATTACK_WITH_ACTIVE") #implement energy requirements later
        
        if player.energy_available:
            actions.append("ATTACH_ENERGY_TO_ACTIVE")

    for card in player.hand:
        if card.card_type == "Pokemon":
            if len(player.bench) is not 3:
                actions.append("PLAY_CARD_" + str(player.hand.index(card)))
        
        elif card.card_type == "Trainer":
            if card.is_supporter:
                if state.supporter_played:
                    actions.append("PLAY_CARD_" + str(player.hand.index(card)))

            else:
                actions.append("PLAY_CARD_" + str(player.hand.index(card)))

    return actions

def apply_action(state: GameState, action:str) -> GameState:

    """
Modifies a GameState depending on what action was selected.

Actions:
    "END_TURN"                  - switches to the other player. increments turn count by 1. resets the supporter_played flag.
    "ATTACH_ENERGY_TO_ACTIVE"   - increments energy counter of active pokemon by 1. Empties the energy zone so attaching happens only once per turn.
    "ATTACK_WITH_ACTIVE"        - decrease opponent's HP by the amount of damage the attack inflicts. ends turn (see END_TURN).
    """
    
    nstate = copy_state(state)

    current_player = nstate.current_player
    player = nstate.player1 if current_player == 1 else nstate.player2
    opponent = nstate.player1 if current_player == 2 else nstate.player2   

    if action == "END_TURN":
        nstate.current_player = (current_player % 2) + 1
        nstate.turn += 1
        nstate.supporter_played = False

    elif action == "ATTACH_ENERGY_TO_ACTIVE":
        player.active.attached_energy += 1
        player.energy_available = False

    elif action == "ATTACK_WITH_ACTIVE":
        opponent.active.hp -= player.active.damage
        nstate.current_player = (current_player % 2) + 1
        nstate.turn += 1

    return nstate

def copy_state(state: GameState) -> GameState:

    """
Duplicate a GameState to modify it whilst not breaking search algorithms later.
    """

    return deepcopy(state)