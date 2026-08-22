from src.models.game_state import GameState
from src.rules.actions import generate_actions, apply_action
from src.solver.evaluator import evaluate_state

def minimax(state: GameState, depth: int, alpha: float, beta: float, maximizing_player: bool) -> int:
    if depth == 0 or state.game_over:
        return evaluate_state(state)
    
    if maximizing_player:
        max_value = -float('inf')
        for action in generate_actions(state):
            new_state = apply_action(state, action)
            value = minimax(new_state, depth-1, alpha, beta, False)
            max_value = max(max_value, value)
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Prune!
        return max_value
    else:
        min_value = float('inf')
        for action in generate_actions(state):
            new_state = apply_action(state, action)
            value = minimax(new_state, depth-1, alpha, beta, True)
            min_value = min(min_value, value)
            beta = min(beta, value)
            if alpha >= beta:
                break  # Prune!
        return min_value

def find_best_move(state: GameState, depth: int) -> str:
    actions = generate_actions(state)
    
    best_action = actions[0]
    best_value = -float('inf')
    alpha = -float('inf')
    beta = float('inf')
    
    for action in actions:
        new_state = apply_action(state, action)
        value = minimax(new_state, depth-1, alpha, beta, False)
        if value > best_value:
            best_value = value
            best_action = action
        alpha = max(alpha, value)
    
    return best_action