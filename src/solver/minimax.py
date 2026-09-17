from src.models.game_state import GameState
from src.rules.actions import apply_action, generate_actions
from src.solver.evaluator import evaluate_from_perspective
from src.solver.move_ordering import order_moves

def search(state: GameState, depth: int, alpha=float('-inf'), beta=float('inf'), player=None, is_maximizing: bool = True):

    if player == None: player = state.current_player

    if depth == 0 or state.game_over:
        return evaluate_from_perspective(state, player), []

    if is_maximizing: # Hero's Turn
        best_score = float('-inf')
        best_first_move = []

        for action in order_moves(generate_actions(state)):
            nstate = apply_action(state, action)

            turn_ended = (nstate.current_player != state.current_player)

            if turn_ended:
                score,_ = search(nstate, depth-1, alpha, beta, player, False)
            else:
                score,_ = search(nstate, depth, alpha, beta, player, True)

            print(f"[depth={depth}] Score for {action} from {'Hero' if is_maximizing else 'Villain'} is {score}.")

            if score > best_score:
                best_score = score
                alpha = score
                best_first_move = action
                if alpha >= beta: break

        return best_score, best_first_move

    else:
        best_score = float('inf')
        best_first_move = []

        for action in order_moves(generate_actions(state)):
            nstate = apply_action(state, action)

            turn_ended = (nstate.current_player != state.current_player)

            if turn_ended:
                score,_ = search(nstate, depth-1, alpha, beta, player, True)
            else:
                score,_ = search(nstate, depth, alpha, beta, player, False)

            print(f"[depth={depth}] Score for {action} from {'Hero' if is_maximizing else 'Villain'} is {score}.")

            if score < best_score:
                best_score = score
                beta = score
                if beta <= alpha: break

        return best_score, best_first_move