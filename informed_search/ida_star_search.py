GRAPH = {
    "S": [("A", 4), ("B", 10), ("C", 11)],
    "A": [("B", 8), ("D", 5)],
    "B": [("D", 15)],
    "C": [("D", 8), ("F", 2), ("E", 20)],
    "D": [("H", 16), ("I", 20), ("F", 1)],
    "E": [("G", 19)],
    "F": [("G", 13)],
    "H": [("I", 1), ("J", 2)],
    "I": [("J", 5), ("K", 13), ("G", 5)],
    "J": [("K", 7)],
    "K": [("G", 16)],
}

H = {
    "S": 7, "A": 8, "B": 6, "C": 5,
    "D": 4, "E": 3, "F": 3, "G": 0,
    "H": 5, "I": 4, "J": 5, "K": 3,
}


def successor(state):
    return GRAPH.get(state, [])


def heuristic(state):
    return H[state]


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
            next_limit = min(next_limit, f)
            continue
        
        if state == g:
            return _path(link), limit
        
        for next_state, step_cost in reversed(successor(state)):
            if next_state not in _ancestors(link):
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


print(ida("S", successor, "G", heuristic))