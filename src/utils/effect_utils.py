from src.models.effect import Effect
from src.models.game_state import GameState

def get_effect_targets(state: GameState, effect: Effect) -> list[str]:

    """
Check where an effect can be applied.
    """

    player = state.player1 if state.current_player == 1 else state.player2
    opponent = state.player2 if state.current_player == 1 else state.player1

    targets = []

    tdict = {
    "active": [player.active],
    "bench": player.bench,
    "any": [player.active] + player.bench,
    "all_own": [player.active] + player.bench,
    "opp_bench": opponent.bench
    }

    if effect.target_condition:

        if effect.target_condition == "typing":

            for slot in tdict[effect.target]:
                if slot.typing == effect.target_condition_instance:
                    targets.append(f"ACTIVE" if slot == player.active else str(player.bench.index(slot)))
    
        elif effect.target_condition == "healable":

            for slot in tdict[effect.target]:
                if slot.hp < slot.max_hp:
                    targets.append(f"ACTIVE" if slot == player.active else str(player.bench.index(slot)))
    
    else:
        for slot in tdict[effect.target]:
            targets.append(f"ACTIVE" if slot == player.active else str(player.bench.index(slot)))

    return targets