from src.rules.actions import generate_actions, apply_action
from src.models.game_state import GameState

def get_turn_sequences(state: GameState, current_sequence=None, sequences=None) -> list[list[str]]:

    """
Recursively generate all possible variations of a turn.
Every sequence ends with END_TURN.
    """

    if current_sequence is None:
        current_sequence = []
    if sequences is None:
        sequences = []

    # Generate all legal actions from the current state
    actions = generate_actions(state)

    for action in actions:
        if action == "END_TURN" or action.startswith("ATTACK"):
            # Record the complete sequence (including END_TURN)
            sequences.append(current_sequence + [action])
            # -> this ends the recursion
        else:
            # Apply the action to get a new state
            new_state = apply_action(state, action)  # assumes this returns a new state
            # Recurse with the new state and the extended sequence
            get_turn_sequences(new_state, current_sequence + [action], sequences)

    return sequences