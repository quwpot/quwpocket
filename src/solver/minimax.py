from src.models.game_state import GameState
from src.rules.actions import generate_actions, apply_action

def minimax(state: GameState, depth: int, maximizing_player: bool) -> int:
    if depth == 0 or state.game_over:
        return evaluate_state(state)
    
    if maximizing_player:
        max_value = -float('inf')
        for action in generate_actions(state):
            new_state = apply_action(state, action)
            value = minimax(new_state, depth-1, False)
            max_value = max(max_value, value)
        return max_value
    else:
        min_value = float('inf')
        for action in generate_actions(state):
            new_state = apply_action(state, action)
            value = minimax(new_state, depth-1, True)
            min_value = min(min_value, value)
        return min_value

def find_best_move(state: GameState, depth: int) -> Action:
    best_action = None
    best_value = -float('inf')
    
    for action in generate_actions(state):
        new_state = apply_action(state, action)
        value = minimax(new_state, depth-1, False)
        if value > best_value:
            best_value = value
            best_action = action
    
    return best_action