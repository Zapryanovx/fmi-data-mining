import os
import sys
import time
from math import isqrt

WIDTH = 0
NEIGHBOURS = ()
DIST = ()

def setup(goal, width):
    global WIDTH, NEIGHBOURS, DIST
    
    WIDTH = width
    size = len(goal)
    
    home = [0] * size
    for position, value in enumerate(goal):
        home[value] = position
        
    DIST = tuple(
        tuple(abs(position // width - home[value] // width)
              + abs(position % width - home[value] % width)
              for value in range(size))
        for position in range(size)
    )
    
    moves = []
    for position in range(size):
        row, col = divmod(position, width)
        
        options = []
        if col + 1 < width:
            options.append(position + 1)
        if col > 0:
            options.append(position - 1)
        if row + 1 < width:
            options.append(position + width)
        if row > 0:
            options.append(position - width)
            
        moves.append(tuple(options))
    
    NEIGHBOURS = tuple(moves)
    
    
def successor(state):
    blank = state.index(0)
    out = []
    
    for tile in NEIGHBOURS[blank]:
        board = list(state)
        board[blank] = board[tile]
        board[tile] = 0
        out.append((tuple(board), 1))
        
    return out


def heuristic(state):
    total = 0
    
    for position, value in enumerate(state):
        if value:
            total += DIST[position][value]
            
    return total


def _ancestors(link):
    while link is not None:
        state, link = link
        yield state
        

def _path(link):
    return list(reversed(list(_ancestors(link))))


def _flimited(s, successor, g, h, limit):
    frontier = [s]
    metadata = [(None, 0)]
    next_limit = float("inf")
    
    while frontier:
        state = frontier.pop()
        parent, cost = metadata.pop()
        link = (state, parent)
        
        f = cost + h(state)
        if f > limit:
            if f < next_limit:
                next_limit = f
            continue
        
        if state == g:
            return _path(link), limit
        
        previous = parent[0] if parent is not None else None
        
        for next_state, step_cost in reversed(successor(state)):
            if next_state != previous:
                frontier.append(next_state)
                metadata.append((link, cost + step_cost))
                
    return None, next_limit


def ida(s, successor, g, h):
    limit = h(s)
    
    while limit < float("inf"):
        path, limit = _flimited(s, successor, g, h, limit)
        
        if path is not None:
            return path
        
    return None


def build_goal(n, index):
    if index == -1:
        index = n
        
    goal = []
    value = 1
    
    for position in range(n + 1):
        if position == index:
            goal.append(0)
        else:
            goal.append(value)
            value += 1
            
    return tuple(goal)


def is_solvable(board, goal, width):
    home = {value: position for position, value in enumerate(goal)}
    permutation = [home[value] for value in board]

    inversions = 0
    for a in range(len(permutation)):
        for b in range(a + 1, len(permutation)):
            if permutation[a] > permutation[b]:
                inversions += 1

    here = board.index(0)
    there = goal.index(0)
    steps = abs(here // width - there // width) + abs(here % width - there % width)

    return inversions % 2 == steps % 2


def directions(path):
    names = []

    for before, after in zip(path, path[1:]):
        step = after.index(0) - before.index(0)

        if step == 1:
            names.append("left")
        elif step == -1:
            names.append("right")
        elif step == WIDTH:
            names.append("up")
        else:
            names.append("down")

    return names


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    index = int(data[1])
    board = tuple(int(token) for token in data[2:2 + n + 1])

    width = isqrt(n + 1)
    goal = build_goal(n, index)
    setup(goal, width)

    started = time.perf_counter()
    path = ida(board, successor, goal, heuristic) if is_solvable(board, goal, width) else None
    elapsed = (time.perf_counter() - started) * 1000

    print(f"# TIMES_MS: alg={elapsed:.3f}")

    if os.environ.get("FMI_TIME_ONLY") == "1":
        return

    if path is None:
        print(-1)
        return

    moves = directions(path)
    sys.stdout.write(f"{len(moves)}\n")

    if moves:
        sys.stdout.write("\n".join(moves) + "\n")


main()
    