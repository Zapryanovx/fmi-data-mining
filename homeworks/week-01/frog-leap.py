import os
import sys
import time


DEAD_ENDS = (">><<", "><<>", "<>><", "><<_", "_>><")


def successors(state):
    i = state.index("_") # free cell
    
    n = len(state)
    out = []
    
    for d in (-1, -2, 1, 2): # candidates for free cell
        j = i + d
        if 0 <= j < n:
            frog = state[j]
            if (d < 0 and frog == ">") or (d > 0 and frog == "<"):
                chars = list(state)
                chars[i], chars[j] = chars[j], chars[i]
                out.append("".join(chars))
                
    return out


def is_dead(state):
    for pattern in DEAD_ENDS:
        if pattern in state:
            return True
    return False    
    
    
def solve(n):
    start = ">" * n + "_" + "<" * n
    goal = "<" * n + "_" + ">" * n
    
    
    # if n == 0 edge case
    if start == goal:
        return [start]
    
    path = [start]
    stack = [iter(successors(start))]
    
    while stack:
        next_state = next(stack[-1], None)
        if next_state is None:
            stack.pop()
            path.pop()
            continue
        
        if is_dead(next_state):
            continue
            
        path.append(next_state)
        
        if next_state == goal:
            return path
        
        stack.append(iter(successors(next_state)))
        
    return None


def main():
    n = int(sys.stdin.readline())
    
    started = time.perf_counter()
    path = solve(n)
    elapsed = (time.perf_counter() - started) * 1000
    
    print(f"# TIMES_MS: alg={elapsed:.3f}")
    
    if os.environ.get("FMI_TIME_ONLY") != "1":
        sys.stdout.write("\n".join(path) + "\n")

main()