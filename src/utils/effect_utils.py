from src.models.effect import Effect

def get_effect_targets(state: GameState, effect: Effect) -> list[str]:

    """
Check where an effect can be applied.
    """

    player = state.player1 if state.current_player == 1 else state.player2

    targets = []


    if effect.target_condition == "typing":

        if player.active and player.active.typing == effect.target_condition_instance:
            targets.append("ACTIVE")

        for i, pokemon in enumerate(player.bench):
            if bench_pokemon.typing == effect.target_condition_instance:
                targets.append(str(i))

        return targets
    
    if effect.target_condition == "healable":

        if player.active.hp < player.active.max_hp:
            targets.append("ACTIVE")

        for i, pokemon in enumerate(player.bench):
            if pokemon.hp < pokemon.max_hp:
                targets.append(str(i))

        return targets
    
    # Add more conditions as needed