from src.models.card import Pokemon, Trainer
from src.models.game_state import PlayerState, GameState
from src.models.effect import Effect
from copy import copy


def copy_pokemon(pk) -> Pokemon | None:

    if pk == None: return None
    
    n_pk = Pokemon(
    name=pk.name,
    card_type=pk.card_type,
    max_hp=pk.max_hp,
    hp=pk.hp,
    typing=pk.typing,
    stage=pk.stage,
    retreat_cost=pk.retreat_cost,
    weakness=pk.weakness,
    evolves_from=pk.evolves_from,
    turns_in_play=pk.turns_in_play,
    is_ex=pk.is_ex,
    special_conditions=pk.special_conditions,
    attached_energy=[energy for energy in pk.attached_energy],
    attacks=list(pk.attacks),
    ability=copy_ability(pk.ability),
    ability_used_this_turn=pk.ability_used_this_turn
    )
    
    return n_pk

def copy_trainer(t) -> Trainer:
    n_trainer = Trainer(
    name=t.name,
    card_type=t.card_type,
    effect=copy_effect(t.effect),
    description=t.description,
    is_supporter=t.is_supporter
    )

    return n_trainer

def copy_player(p) -> PlayerState:
    n_p = PlayerState(
    active=copy_pokemon(p.active),
    bench=[copy_pokemon(pokemon) for pokemon in p.bench],
    hand=list(p.hand),
    deck=list(p.deck),
    points=p.points,
    energy_types=p.energy_types,
    next_energy_type=p.next_energy_type,
    current_energy_type=p.current_energy_type,
    energy_available=p.energy_available,
    damage_boost=p.damage_boost
    )

    return n_p

def copy_state(state) -> GameState:
    n_state = GameState(
    player1=copy_player(state.player1),
    player2=copy_player(state.player2),
    turn=state.turn,
    current_player=state.current_player,
    game_over=state.game_over,
    winner=state.winner,
    seed=state.seed,
    rng=copy(state.rng),
    supporter_played=state.supporter_played,
    is_first_turn=state.is_first_turn,
    pending_promotion=state.pending_promotion,
    pending_player=state.pending_player
    )

    return n_state

def copy_effect(e) -> Effect:
    n_effect = Effect(
    effect_type=e.effect_type,
    target=e.target,
    amount=e.amount,
    instance=e.instance,
    target_conditions=list(e.target_conditions)
    )

    return n_effect

def copy_ability(a) -> Ability:

    if a == None: return None

    n_ability = Ability(
    name=a.name,
    ability_type=a.ability_type,
    effect=copy_effect(a.effect),
    description=a.description,
    req_active=a.req_active
    )

    return n_ability