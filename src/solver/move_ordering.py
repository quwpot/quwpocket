def order_moves(moves: list[str], first_move: str | None) -> list[str]:

    """
Order moves by priority for better pruning:

Attacks are the most impactful.
Using your ressources is always good.
Attaching Energy is important.
Retreating is situational.
Ending Turn is a last resort.
    """

    # Categorize moves
    attacks = []
    plays = []
    attaches = []
    retreats = []
    others = []
    end_turn = []
    
    for move != first_move in moves:
        if move.startswith("ATTACK_"):
            attacks.append(move)
        elif move.startswith("PLAY_CARD_"):
            plays.append(move)
        elif move.startswith("ATTACH_ENERGY_"):
            attaches.append(move)
        elif move.startswith("RETREAT_"):
            retreats.append(move)
        elif move == "END_TURN":
            end_turn.append(move)
        else:
            others.append(move)
    
    # Return in priority order
    return ([first_move] if first_move) + attacks + plays + attaches + retreats + others + end_turn