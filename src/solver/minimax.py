from src.models.game_state import GameState
from src.rules.actions import apply_action, generate_actions
from src.solver.evaluator import evaluate_from_perspective
from src.solver.move_ordering import order_moves
from time import perf_counter

_node_count = 0
_time_apply = 0
_time_generate = 0
_time_order = 0
_prune_count = 0


def search(state: GameState, depth: int, first_move=None,
           alpha=float('-inf'), beta=float('inf'),
           player=None, is_maximizing: bool = True, debug: bool = False):

    global _node_count, _time_apply, _time_generate, _time_order, _prune_count

    _node_count += 1

    if player is None:
        player = state.current_player

    if depth == 0 or state.game_over:
        return evaluate_from_perspective(state, player), []

    # Sign flips depending on whose turn it is
    best_score = float('-inf') if is_maximizing else float('inf')
    best_first_move = []

    t = perf_counter()
    actions = generate_actions(state)
    _time_generate += perf_counter() - t

    t = perf_counter()
    ordered = order_moves(actions, first_move)
    _time_order += perf_counter() - t

    for action in ordered:

        t = perf_counter()
        nstate = apply_action(state, action)
        _time_apply += perf_counter() - t

        turn_ended = (nstate.current_player != state.current_player)
        next_depth = depth - 1 if turn_ended else depth
        next_is_max = (not is_maximizing) if turn_ended else is_maximizing

        score, _ = search(
            nstate,
            next_depth,
            alpha=alpha,
            beta=beta,
            player=player,
            is_maximizing=next_is_max,
        )

        if debug:
            side = 'Hero' if is_maximizing else 'Villain'
            print(f"[depth={depth}] Score for {action} from {side} is {score}.")

        # Both branches collapse to: "is this score better than the current best?"
        if (is_maximizing and score > best_score) or \
           (not is_maximizing and score < best_score):
            best_score = score
            best_first_move = action

            # Update the bound that corresponds to this side
            if is_maximizing:
                alpha = max(alpha, score)
            else:
                beta = min(beta, score)

            if alpha >= beta:
                _prune_count += 1
                break

    return best_score, best_first_move


def find_best_move(state, depth):
    _, action = search(state, depth, player=state.current_player)
    return action


def get_node_count():
    return _node_count
def get_prune_count():
    return _prune_count


def reset_node_count():
    global _node_count
    _node_count = 0
def reset_prune_count():
    global _prune_count
    _prune_count = 0


def reset_timers():
    global _time_apply, _time_generate, _time_order
    _time_apply = 0
    _time_generate = 0
    _time_order = 0

def get_time_apply():
    return _time_apply
def get_time_generate():
    return _time_generate
def get_time_order():
    return _time_order