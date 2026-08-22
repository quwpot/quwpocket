from src.models.game_state import GameState

def evaluate_from_perspective(state: GameState, player: int) -> int:
    score = 0
    
    hero = state.player1 if player == 1 else state.player2
    villain = state.player2 if player == 1 else state.player1
    
    score += (3 * hero.points)
    score += (3 * (3 - villain.points))
    score += (4 * len(hero.bench))
    
    total_energy_hero = 0
    total_low_hp = 0

    for card in [hero.active] + hero.bench:
        total_energy_hero += len(card.attached_energy)
        if (card.max_hp - card.hp) < (card.max_hp * 0.25): #pokemon counts as low if it has less then 25% HP remaining
            total_low_hp += 1
 
    score += (5 * total_energy_hero)
    
    score += (2 * len(hero.hand)) #more cards in hand = good

    #score += (hero.active.attacks[-1].damage / 10) #better attacks on active = good

    score -= (5 * total_low_hp) #pokemon with low hp = bad

    if hero.active.stage == "stage1": #stage 1 boost (bigger = better)
        score += 5
    if hero.active.stage == "stage2": #stage 2 boost
        score += 8

    score -= (4 * hero.active.retreat_cost)

    if not hero.bench:
        score -= 8

    return score

def evaluate_state(state: GameState) -> int:
    """Evaluate state from current player's perspective."""
    current_player = state.current_player
    return evaluate_from_perspective(state, current_player)