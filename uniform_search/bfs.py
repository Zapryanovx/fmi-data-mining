from collections import deque

TREE = {
    "S": [("A", 1), ("B", 4), ("C", 2)],
    "A": [("D", 2), ("E", 3)],
    "C": [("F", 1), ("G2", 5)],
    "D": [("G1", 1)],
}


def successor(state):
    return TREE.get(state, [])


def _ancestors(link):
    while link is not None:
        state, link = link
        yield state


def _path(link):
    return list(reversed(list(_ancestors(link))))


def bfs(s, successor, g):
    frontier = deque([s])
    parents = {s: (s, None)}
    
    while frontier:
        state = frontier.popleft()
        
        if state == g:
            return _path(parents[state])
        
        for next_state, _ in successor(state):
            if next_state not in parents:
                parents[next_state] = (next_state, parents[state])
                frontier.append(next_state)
                
    return None

print(bfs("S", successor, "G1"))