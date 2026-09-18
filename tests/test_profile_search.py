"""Profile the solver on a saved mid-game state.

First run: creates tests/profile_state.pkl by playing a few turns.
Subsequent runs: loads the pickle and profiles search() on it.
"""

import sys
import os
import pickle
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.game_state import create_initial_state
from src.rules.deck_builder import build_deck
from src.rules.actions import apply_action, generate_actions
from src.solver.minimax import (
    search,
    get_node_count, reset_node_count,
    reset_timers,
    get_time_apply, get_time_generate, get_time_order
)

PICKLE_PATH = os.path.join(os.path.dirname(__file__), "profile_state.pkl")
SEED = 42
DEPTH = 2


def build_decks():
    """Same decks as game_runner uses."""
    p1_deck = build_deck([
        "Pokeball", "Pokeball", "Professors Research", "Professors Research",
        "Potion", "Weedle", "Weedle", "Kakuna", "Kakuna", "Beedrill", "Beedrill"
    ])
    p2_deck = build_deck([
        "Pokeball", "Pokeball", "Professors Research", "Professors Research",
        "Potion", "Erika", "Erika", "Exeggcute", "Exeggcute", "Exeggutor", "Exeggutor"
    ])
    return p1_deck, p2_deck


def create_and_save_state():
    """Play a few turns by always picking the first legal action, then save."""
    p1_deck, p2_deck = build_decks()
    state = create_initial_state(p1_deck, p2_deck, ["Grass"], seed=SEED)

    # Play until we've seen ~3 turns. Fast — no solver involved.
    safety = 0
    while state.turn < 3 and not state.game_over and safety < 200:
        actions = generate_actions(state)
        if not actions:
            break
        state = apply_action(state, actions[0])
        safety += 1

    with open(PICKLE_PATH, "wb") as f:
        pickle.dump(state, f)

    print(f"Saved profile state to {PICKLE_PATH}")
    print(f"  turn={state.turn}, current_player={state.current_player}")
    return state


def load_state():
    if not os.path.exists(PICKLE_PATH):
        return create_and_save_state()
    with open(PICKLE_PATH, "rb") as f:
        state = pickle.load(f)
    print(f"Loaded profile state from {PICKLE_PATH}")
    print(f"  turn={state.turn}, current_player={state.current_player}")
    return state


def run_profile(state, depth=DEPTH):
    """Run search once and report timing breakdown."""
    reset_node_count()
    reset_timers()

    t0 = time.perf_counter()
    score, move = search(state, depth=depth, player=state.current_player)
    total = time.perf_counter() - t0

    nodes = get_node_count()

    # These getters must exist in minimax.py:
    t_apply = get_time_apply()
    t_gen = get_time_generate()
    t_ord = get_time_order()
    t_other = total - t_apply - t_gen - t_ord

    def pct(t):
        return f"{100 * t / total:.1f}%" if total > 0 else "n/a"

    print()
    print("=" * 55)
    print(f"PROFILE — depth={depth}, seed={SEED}")
    print("=" * 55)
    print(f"Best move:              {move}")
    print(f"Score:                  {score}")
    print()
    print(f"Total nodes:            {nodes:,}")
    print(f"Total time:             {total:.3f} s")
    print(f"Nodes per second:       {nodes / total:,.0f}" if total > 0 else "n/a")
    print()
    print(f"Time breakdown:")
    print(f"  apply_action:         {t_apply:.3f} s  ({pct(t_apply)})")
    print(f"  generate_actions:     {t_gen:.3f} s  ({pct(t_gen)})")
    print(f"  order_moves:          {t_ord:.3f} s  ({pct(t_ord)})")
    print(f"  other (eval, loop):   {t_other:.3f} s  ({pct(t_other)})")
    print()
    if nodes > 0:
        print(f"Per node:")
        print(f"  apply_action:         {1000 * t_apply / nodes:.3f} ms")
        print(f"  generate_actions:     {1000 * t_gen / nodes:.3f} ms")
        print(f"  order_moves:          {1000 * t_ord / nodes:.3f} ms")
        print(f"  total:                {1000 * total / nodes:.3f} ms")
    print("=" * 55)


if __name__ == "__main__":
    state = load_state()
    run_profile(state, depth=DEPTH)