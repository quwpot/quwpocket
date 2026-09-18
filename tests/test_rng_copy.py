"""Verify copy_state RNG is truly independent."""

import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.game_state import create_initial_state
from src.rules.deck_builder import build_deck
from src.rules.copy import copy_state

def make_state():
    p1 = build_deck(["Weedle"] * 20)
    p2 = build_deck(["Weedle"] * 20)
    return create_initial_state(p1, p2, ["Grass"], seed=42)

def test_rng_truly_independent():
    """Advance the copy's RNG; state's next draw must be unchanged."""
    state = make_state()

    # Baseline: what does state's RNG produce as its first draw?
    state.rng.seed(12345)
    baseline = state.rng.random()

    # Reset, copy, advance the copy
    state.rng.seed(12345)
    s2 = copy_state(state)
    _ = s2.rng.random()  # consume one from the copy

    # State's next draw must still equal the baseline
    after = state.rng.random()
    print(f"baseline: {baseline}")
    print(f"after copy consumed one: {after}")
    assert baseline == after, "RNG state leaked between copy and original"
    print("✅ copy_state RNG is truly independent")

if __name__ == "__main__":
    test_rng_truly_independent()