from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class PlayerState:

    """
PlayerState tracks all relevant information on one player's side of the board.

Attributes:
    active: the pokemon currently in active position.
    bench: a list of all pokemon currently on the bench (max bench size = 3).
    hand: a list of all cards currently in hand.
    deck: a list of all remaining cards in deck (in draw order).
    points: the amount  of KO's the player has already taken. First to reach 3 points wins.
    energy_type: what kinds of energy get generated in the energy zone
    energy_available: if the player can still attach an energy from the energy zone this turn. Energies do not carry over to future turns and can be attached to any pokemon of choice.
    """

    active: Pokemon | None = None
    bench: list[Pokemon] = field(default_factory = list)
    hand: list[Card] = field(default_factory = list)
    deck: list[Card] = field(default_factory = list)
    discard: list[Card] = field(default_factory = list)
    points: int = 0
    energy_type: str = ""
    energy_available: bool = False
    damage_boost: Optional[int] = 0

@dataclass
class GameState:

    """
Class that represents the entire Game. Every information gets tracked here.

Attributes:
    player1: all information on player1's side of the board.
    player2: all information on player2's side of the board.
    turn: how many turns have passed since the beginning of the game.
    current_player: Whose turn it is. Only the active player may take actions.
    game_over: True if someone has reached 3 points through knockouts.
    winner: The player that triggered the end of the game (i.e. the one that reached 3 points)
    supporter_played: If a Supporter card was already played this turn. Only one supporter card may be played each turn.
    """

    player1: PlayerState 
    player2: PlayerState
    turn: int
    current_player: int
    game_over: bool
    winner: int | None
    supporter_played: bool = False

def create_initial_state(energy_type: str = "Fire") -> GameState:
    
    """
Helper function that sets up a game by initializing a default GameState.
    """

    p1 = PlayerState(energy_type=energy_type)
    p2 = PlayerState(energy_type=energy_type)
    return GameState(
        player1=p1,
        player2=p2,
        turn=1,
        current_player=1,
        game_over=False,
        winner=None,
        supporter_played=False
    )