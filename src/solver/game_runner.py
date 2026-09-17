from src.rules.deck_builder import build_deck
from src.rules.actions import apply_action
from src.solver.solver_wrapper import solve_with_time_limit, start_poller, poll_nodes
from src.models.game_state import create_initial_state
from time import time
from tqdm import tqdm

def play_game(solver_depth, max_turns=50):
    p1_deck = build_deck(["Pokeball", "Pokeball", "Professors Research", "Professors Research", "Potion", "Weedle", "Weedle", "Kakuna", "Kakuna", "Beedrill", "Beedrill"])
    p2_deck = build_deck(["Pokeball", "Pokeball", "Professors Research", "Professors Research", "Potion", "Erika", "Erika", "Exeggcute", "Exeggcute", "Exeggutor", "Exeggutor"])

    state = create_initial_state(p1_deck, p2_deck, ["Grass"], debug=True)

    pbar = tqdm(total=None, desc="Game")
    while not state.game_over:

        pbar.set_postfix({"p1": state.player1.points, "p2": state.player2.points, "Turn": state.turn})
        stop_event, poller_thread = start_poller(pbar)

        action, stats = solve_with_time_limit(state, solver_depth, 30)
        if action is None:
            break

        stop_event.set()
        poller_thread.join()
        pbar.update(1)

        tqdm.write(f"Turn {state.turn}: P{state.current_player} plays {action} "
                   f"(depth {stats['depth_reached']}, {stats['nodes']} nodes, {stats['time']:.1f}s)")

        state = apply_action(state, action)    

    pbar.close()

    print(f"Player {state.winner} won with "
          f"{state.player1.points if state.winner == 1 else state.player2.points} points "
          f"after {state.turn} turns.")

 