"""Verify custom copy_state produces identical search results to deepcopy."""

import sys
import os
import pickle
from copy import deepcopy
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import src.rules.actions as actions_module
from src.models.game_state import create_initial_state
from src.rules.deck_builder import build_deck
from src.rules.copy import copy_state as fast_copy
from src.solver.minimax import search, reset_node_count, get_node_count

PICKLE_PATH = os.path.join(os.path.dirname(__file__), "profile_state.pkl")

def load_or_make_state():
    if os.path.exists(PICKLE_PATH):
        with open(PICKLE_PATH, "rb") as f:
            state = pickle.load(f)
        print(f"Loaded pickle: turn={state.turn}, cp={state.current_player}")
        return state

    # Fallback: make a fresh state and play a few actions
    from src.rules.actions import generate_actions, apply_action
    p1 = build_deck(["Weedle", "Weedle", "Kakuna", "Kakuna", "Beedrill", "Beedrill"] * 3 + ["Potion"] * 2)
    p2 = build_deck(["Exeggcute", "Exeggcute", "Exeggutor", "Exeggutor"] * 4 + ["Potion"] * 4)
    state = create_initial_state(p1, p2, ["Grass"], seed=42)

    safety = 0
    while state.turn < 3 and not state.game_over and safety < 200:
        acts = generate_actions(state)
        if not acts:
            break
        state = apply_action(state, acts[0])
        safety += 1
    return state

def run_with(copy_fn, state, label):
    """Monkey-patch actions_module.copy_state, then run search."""
    original = actions_module.copy_state
    actions_module.copy_state = copy_fn
    try:
        reset_node_count()
        score, move = search(state, depth=2, player=state.current_player)
        nodes = get_node_count()
    finally:
        actions_module.copy_state = original
    print(f"{label}: score={score}, move={move}, nodes={nodes}")
    return score, move, nodes

if __name__ == "__main__":
    state = load_or_make_state()

    print("=" * 55)
    print("COPY-STATE EQUIVALENCE")
    print("=" * 55)

    score_ref, move_ref, nodes_ref = run_with(deepcopy, state, "deepcopy ref ")
    score_fst, move_fst, nodes_fst = run_with(fast_copy, state, "fast copy   ")

    print()
    print(f"Score match: {score_ref == score_fst}")
    print(f"Move  match: {move_ref == move_fst}")
    print(f"Nodes match: {nodes_ref == nodes_fst}")
    print()
    if score_ref == score_fst and move_ref == move_fst and nodes_ref == nodes_fst:
        print("✅ Custom copy is behavior-equivalent to deepcopy")
    else:
        print("❌ Copy is not equivalent — bug to fix")
    print("=" * 55)