from copy import deepcopy
from src.models.game_state import GameState
from src.models.effects import *
from src.utils.energy_utils import can_use_attack
from src.utils.effect_utils import get_effect_targets
from random import choice

def generate_actions(state: GameState, debug: bool = False) -> list[str]:

    """
Returns a list of all possible actions (draw card, attach energy, attack, ...) from a current GameState.

1. Checks whose turn it is
2. Grab the representative PlayerState
3. Check which actions are possible.

Actions:
    "PROMOTE_FROM_BENCH_N"                          - after knockout
    "END_TURN"                                      - always possible.
    "ATTACH_ENERGY_TO_SLOT_N"                       - possible if: energy zone still contains energy (i.e. no energy was attached yet).
    "ATTACK_N"                                      - possible if: active pokemon has fulfilled the energy requirement for its attack AND is not asleep.
    "PLAY_CARD_N" (for each card in hand)           - possible if: card is basic pokemon/fossil and bench is not full  OR card is evolutiom pokemon and preevolution exists OR card is Item OR card is Supporter and no supporter was played yet.
    "RETREAT_TO_SLOT_N" (for each Pokemon on Bench) - possible if: active pokemon has enough energy, bench is non-empty (replacement exists) AND active pokemon is  not asleep.
    "DISCARD_FOSSIL_N" (slot n)                     - possible if: fossil is in play.
    "USE_ABILITY_N" (slot n)                        - possible if: card has ability and can use it (e.g. requirements: card needs to be in active, ability cann only be used once per turn, ...)
    """

    current_player = state.current_player
    player = state.player1 if current_player == 1 else state.player2    
    
    actions = ["END_TURN"]

    if state.pending_promotion:
        player = state.player1 if state.pending_player == 1 else state.player2
        actions = []
        for i in range(len(player.bench)):
            actions.append(f"PROMOTE_FROM_BENCH_{i}")
        return actions

    if player.active:

        if debug:
            print(f"Player has an active Pokemon")

        if player.active.card_type == "pokemon":

            if not player.active.special_conditions & (1 << 1):

                for i, attack in enumerate(player.active.attacks):
                    if can_use_attack(player.active, attack):

                        if attack.needs_target:

                            targets = get_effect_targets(state, attack.effect)
                            if targets:
                                for target in targets:
                                    actions.append(f"ATTACK_{target}_{i}")
                            else:
                                actions.append(f"ATTACK_{i}")

                        else: actions.append(f"ATTACK_{i}")

                if len(player.active.attached_energy) >= player.active.retreat_cost:
                    for i, card in enumerate(player.bench):
                        actions.append(f"RETREAT_TO_SLOT_{i}")
        
            if player.energy_available:
                actions.append("ATTACH_ENERGY_TO_SLOT_ACTIVE")

            if player.active.ability and player.active.ability.ability_type not in ["passive"]:
                if (player.active.ability.ability_type == "once_per_turn" and not player.active.ability.used_this_turn) or player.active.ability.ability_type == "infinite":
                    targets = get_effect_targets(state, player.active.ability.effect)
                    if targets:
                        if player.active.ability.effect.target != "all_own":
                            for target in targets:
                                actions.append(f"USE_ABILITY_{target}_ACTIVE")
                        else:
                            actions.append(f"USE_ABILITY_ACTIVE")

        elif player.active.card_type == "fossil":
            actions.append("DISCARD_FOSSIL_ACTIVE")

    for i, card in enumerate(player.hand):
        if card.card_type in ["pokemon", "fossil"]:
            if len(player.bench) != 3 and card.stage == "basic":
                actions.append(f"PLAY_CARD_{i}")
                if debug:
                    print(f"Appended 'PLAY_CARD_{i}' to action list. Card name: {card.name}")

            elif card.evolves_from == player.active.name and player.active.turns_in_play >= 1:
                actions.append(f"PLAY_CARD_ACTIVE_{i}")

            for j, dude in enumerate(player.bench):
                if card.evolves_from == dude.name and dude.turns_in_play >= 1:
                    actions.append(f"PLAY_CARD_{j}_{i}")
        
        elif card.card_type == "trainer":

            if card.is_supporter:

                if state.supporter_played:
                    continue

            if card.effect.target_condition:
                targets = get_effect_targets(state, card.effect)

                if not targets: #the effect can't be applied anywhere -> card can't be played
                    continue

                for target in targets:
                    actions.append(f"PLAY_CARD_{target}_{i}")

            else:
                actions.append(f"PLAY_CARD_{i}")

    for i, card in enumerate(player.bench):
        if player.energy_available:
            actions.append("ATTACH_ENERGY_TO_SLOT_" + str(i))

        if card.card_type == "fossil":
            actions.append(f"DISCARD_FOSSIL_" + str(i))

        if card.ability:
            if not card.ability.req_active:

                if not card.ability.used_this_turn and card.ability.ability_type == "once_per_turn" or card.ability.ability_type == "infinite":
                    targets = get_effect_targets(state, card.ability.effect)
                    if targets:
                        if card.ability.effect.target != "all_own":
                            for target in targets:
                                actions.append(f"USE_ABILITY_{target}_{i}")
                        else:
                            actions.append(f"USE_ABILITY_{i}")

    return actions

EFFECT_HANDLERS = {
    "discard_energy": apply_discard_energy,
    "heal": apply_heal,
    "deck_to_hand": apply_deck_to_hand,
    "attach_energy": apply_attach_energy,
    "coin_flip_bonus_damage": apply_coin_flip_bonus_damage,
    "draw": apply_draw,
    "damage_boost": apply_damage_boost,
    "watch_opponent_hand_cards": apply_watch_opponent_hand_cards,
    "discard_energy": apply_discard_energy,
    "switch_opponent_active": apply_switch_opponent_active,
    "special_condition": apply_special_condition
}

def apply_effect(state, effect):
    handler = EFFECT_HANDLERS.get(effect.effect_type)
    if handler is None:
        raise ValueError(f"Unknown effect type: {effect.effect_type}")
    return handler(state, effect)

def apply_action(state: GameState, action:str, debug: bool = False) -> GameState:

    """
Modifies a GameState depending on what action was selected.

Actions:
    "END_TURN"                  - Switches to the other player. increments turn count by 1. resets the supporter_played flag.
    "ATTACH_ENERGY_TO_SLOT_N"   - Adds the current_energy_tpye to the list of attached energies of this Pokemon. Empties the energy zone so attaching happens only once per turn.
    "ATTACK_N"                  - Chooses the attack at slot N and decreases opponent's HP by the amount of damage the attack inflicts. Apply additional effects (if any), check for knockout, end turn (see END_TURN).
    "PLAY_CARD_N"               - Trainer cards: apply effect, discard. Basic Pokemon: add to bench. Evolutions: evolve.
    "RETREAT_TO_SLOT_N"         - Remove special conditions, delete Energy, move active to bench, move benched to active.
    "DISCARD_FOSSIL_N"          - Remove the fossil at the specified slot from play.
    "USE_ABILITY_N"             - Applies the effect of the specified ability.
    "PROMOTE_FROM_BENCH_N"      - Moves new Pokemon into now free acrive slot.
    """
    
    nstate = copy_state(state)

    current_player = nstate.current_player
    player = nstate.player1 if current_player == 1 else nstate.player2
    opponent = nstate.player1 if current_player == 2 else nstate.player2   

    if action == "END_TURN":
        nstate.current_player = (current_player % 2) + 1
        nstate.turn += 1
        nstate = start_turn(nstate)

    elif action.startswith("ATTACH_ENERGY_TO_SLOT_"):
        slot = action.split("_")[-1]

        if slot == "ACTIVE":
            player.active.attached_energy.append(player.current_energy_type)

        else:
            player.bench[int(slot)].attached_energy.append(player.current_energy_type)

        player.current_energy_type = None
        player.energy_available = False

    elif action.startswith("ATTACK_"):
        index = int(action.split("_")[-1])
        target = action.split("_")[-2]
        attack = player.active.attacks[index]

        opponent.active.hp -= (attack.damage + player.damage_boost)
        if opponent.active.weakness == player.active.typing:
            opponent.active.hp -= 20

        if attack.effect:

            neffect = deepcopy(attack.effect)
            neffect.target = target

            nstate = apply_effect(nstate, neffect)
            player = nstate.player1 if current_player == 1 else nstate.player2
            opponent = nstate.player1 if current_player == 2 else nstate.player2

        if opponent.active.hp <= 0:
            if opponent.active.is_ex:
                player.points += 2
            else:
                player.points += 1
            
            opponent.active = None
            
            if player.points >= 3 or (opponent.bench == []):
                nstate.game_over = True
                nstate.winner = current_player
                return nstate

            else:
                nstate.pending_promotion = True
                nstate.pending_player = 2 if current_player == 1 else 1  # Opponent needs to promote
                return nstate

        nstate.current_player = (current_player % 2) + 1
        nstate.turn += 1
        nstate = start_turn(nstate)

    elif action.startswith("PLAY_CARD_"):
        card_index = int(action.split("_")[-1])
        target = action.split("_")[-2]
        card = player.hand[card_index]
        if debug: print(f"{card.name} (Index: {card_index}) gets played.")

        if card.card_type == "trainer":
     
            ncard = deepcopy(card)
            ncard.effect.target = target

            nstate = apply_effect(nstate, ncard.effect)
            player = nstate.player1 if current_player == 1 else nstate.player2
            opponent = nstate.player1 if current_player == 2 else nstate.player2
        
            if card.is_supporter:
                nstate.supporter_played = True

            if debug: print(f"Card {card_index} gets discarded from {[card.name for card in player.hand]}.")
            player.hand.pop(card_index)

        elif card.card_type in ["pokemon", "fossil"]:
    
            if card.stage == "basic":
                player.bench.append(player.hand.pop(card_index))

            else:
    
                if target == "ACTIVE":
                    temp = player.active
                    player.active = player.hand.pop(card_index)
                    player.active.hp = player.active.max_hp - (temp.max_hp - temp.hp)
                    player.active.attached_energy = temp.attached_energy

                else:
                    temp = player.bench.pop(int(target))
                    card = player.hand.pop(card_index)
                    player.bench.insert(int(target), card)
                    player.bench[int(target)].hp = player.bench[int(target)].max_hp - (temp.max_hp - temp.hp)
                    player.bench[int(target)].attached_energy = temp.attached_energy

        player = nstate.player1 if current_player == 1 else nstate.player2       

    elif action.startswith("RETREAT_TO_SLOT_"):
        slot_index = int(action.split("_")[-1])

        player.active.special_conditions = 0

        for i in range(player.active.retreat_cost):
            player.active.attached_energy.pop() #what energy can theoretically be chosen by the player - will implement later

        temp = player.active
        player.active = player.bench.pop(slot_index)
        player.bench.insert(slot_index, temp)

    elif action.startswith("DISCARD_FOSSIL_"):
        slot = action.split("_")[-1]

        if slot == "ACTIVE":
            player.active = None
        
        else:
            player.bench.pop(int(slot))

    elif action.startswith("USE_ABILITY_"):
        parts = action.split("_")
        slot = parts[-1]
        target = parts[-2]

        if slot == "ACTIVE":
            ability = player.active.ability
        else:
            ability = player.bench[int(slot)].ability

        nability = deepcopy(ability)
        nability.effect.target = target

        nstate = apply_effect(nstate, nability.effect)
        player = nstate.player1 if current_player == 1 else nstate.player2
        opponent = nstate.player1 if current_player == 2 else nstate.player2

        # Set used_this_turn on the NEW state's ability
        if slot == "ACTIVE":
            player.active.ability.used_this_turn = True
        else:
            player.bench[int(slot)].ability.used_this_turn = True

    elif action.startswith("PROMOTE_FROM_BENCH_"):
        slot = int(action.split("_")[-1])
        player = nstate.player1 if nstate.pending_player == 1 else nstate.player2
    
        # Move Pokemon from bench to active
        player.active = player.bench.pop(slot)
        nstate.pending_promotion = False
        nstate.pending_player = 0

        nstate.current_player = (current_player % 2) + 1
        nstate.turn += 1
        nstate = start_turn(nstate)

    else:
        raise Exception("Invalid Action")

    return nstate

def copy_state(state: GameState) -> GameState:

    """
Duplicate a GameState to modify it whilst not breaking search algorithms later.
    """

    return deepcopy(state)

def start_turn(state: GameState, debug=False) -> GameState:
    
    """
Apply start-of-turn effects (mutates the state in place).

1. Draw a card (empty deck -> nothing happens)
2. Generate Energy in the Energy Zone based on next_energy_type
3. Calculate which type of energy will be generated next turn
4. Reset supporter_played flag
5. Reset ability_used flag
6. Reset damage_boost
7. Apply special conditions
8. Increment each Pokemon's turns_in_play counter by 1.
    """

    player = state.player1 if state.current_player == 1 else state.player2
    opponent = state.player1 if state.current_player == 2 else state.player2
    if player.deck:
        player.hand.append(player.deck.pop())
    
    player.energy_available = True
    player.current_energy_type = player.next_energy_type
    player.next_energy_type = choice(player.energy_types)

    state.supporter_played = False

    if player.active.ability:
        player.active.ability.used_this_turn = False
    for pokemon in player.bench:
        if pokemon.ability:
            pokemon.ability.used_this_turn = False

    player.damage_boost = 0

    if player.active.special_conditions:

        if player.active.special_conditions & (1 << 0): #poison
            player.active.hp -= 10

            if player.active.hp <= 0:
                if player.active.is_ex:
                    opponent.points += 2
                else:
                    opponent.points += 1
            
                player.active = None
            
                if opponent.points >= 3 or (player.bench == []):
                    state.game_over = True
                    state.winner = 2 if state.current_player == 1 else 1
                    return state

                else:
                    state.pending_promotion = True
                    state.pending_player = current_player
                    return state

        if player.active.special_conditions & (1 << 1): #sleep
            if choice([True, False]):  # Heads = wake up
                player.active.special_conditions -= 2
                if debug:
                    print(f"{player.active.name} woke up!")
            else:
                if debug:
                    print(f"{player.active.name} is still asleep!")

    if player.active:    
        player.active.turns_in_play += 1
    for pokemon in player.bench:
        pokemon.turns_in_play += 1

    if state.is_first_turn:
        player.energy_available = False
        state.is_first_turn = False

    return state