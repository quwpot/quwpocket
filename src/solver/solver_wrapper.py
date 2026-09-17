from time import time, perf_counter
from src.solver.minimax import reset_node_count, find_best_move, get_node_count
import threading

def solve_with_time_limit(state, max_depth: int, time_limit_seconds):

    start_time = time()

    best_move = None

    for d in range(1, max_depth+1):
        reset_node_count()
        start = perf_counter()
        best = find_best_move(state, depth=d)
        elapsed = perf_counter() - start
        nodes = get_node_count()
        nps = nodes/elapsed
        stats = {"depth_reached": d, "nodes": nodes, "time": elapsed, "nps": nps}
        best_move = best
        if elapsed > time_limit_seconds:
            break

    return best_move, stats

def poll_nodes(pbar, stop_event, start_time):
    while not stop_event.is_set():
        nodes = get_node_count()
        elapsed = perf_counter() - start_time
        nps = nodes / elapsed if elapsed > 0 else 0
        pbar.set_postfix({"nodes": nodes, "nps": int(nps)})
        stop_event.wait(0.3)   # sleep up to 300ms, but wake immediately if set

def start_poller(pbar):

    event = threading.Event()

    start = perf_counter()

    thread = threading.Thread(target=poll_nodes, args=(pbar, event, start), daemon=True)
    thread.start()

    return event, thread