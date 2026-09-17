from src.models.game_state import GameState
from src.rules.actions import apply_action
from src.solver.evaluator import evaluate_from_perspective
from src.solver.search import get_turn_sequences

def minimax_turn(state: GameState, depth: int, player=None, is_maximizing: bool = True):

    if player == None: player = state.current_player

    if depth == 0 or state.game_over:
        return evaluate_from_perspective(state, player), []

    if is_maximizing: # Hero's Turn
        best_score = float('-inf')
        best_first_move = []

        for sequence in get_turn_sequences(state):
            nstate = state
            for action in sequence:
                nstate = apply_action(nstate, action)
            # all sequences applied -> opponent's turn
            score,_ = minimax_turn(nstate, depth-1, player, False)

            print(f"[depth={depth}] Score for {sequence} from {'Hero' if is_maximizing else 'Villain'} is {score}.")

            if score > best_score:
                best_score = score
                best_first_move = sequence[0]

        return best_score, best_first_move

    else:
        best_score = float('inf')
        best_first_move = []

        for sequence in get_turn_sequences(state):
            nstate = state
            for action in sequence:
                nstate = apply_action(nstate, action)

            score, _ = minimax_turn(nstate, depth - 1, player, True)

            print(f"[depth={depth}] Score for {sequence} from {'Hero' if is_maximizing else 'Villain'} is {score}.")

            if score < best_score:
                best_score = score
                best_first_move = sequence[0]

        return best_score, best_first_move