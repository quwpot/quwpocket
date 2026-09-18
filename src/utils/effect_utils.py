from src.models.effect import Effect
from src.models.game_state import GameState

def _matches(pokemon, condition: dict) -> bool:
    ctype = condition["type"]
    if ctype == "typing":
        return pokemon.typing == condition["value"]
    if ctype == "healable":
        return pokemon.hp < pokemon.max_hp
    if ctype == "stage":
        return pokemon.stage == condition["value"]
    raise ValueError(f"Unknown condition type: {ctype}")


def get_effect_targets(state: GameState, effect: Effect) -> list[str]:

    """
Check where an effect can be applied.
    """

    player = state.player1 if state.current_player == 1 else state.player2
    opponent = state.player2 if state.current_player == 1 else state.player1

    tdict = {
        "active": [player.active] if player.active else [],
        "bench": player.bench,
        "any": ([player.active] if player.active else []) + player.bench,
        "all_own": ([player.active] if player.active else []) + player.bench,
        "opp_bench": opponent.bench,
    }

    slots = tdict[effect.target]
    targets = []

    for slot in slots:
        if slot is None:
            continue
        if all(_matches(slot, c) for c in effect.target_conditions):
            targets.append("ACTIVE" if slot is player.active else str(player.bench.index(slot)))

    return targets