from heapq import heappop, heappush

TREE = {
    "S": [("A", 1), ("G", 5)],
    "A": [("G", 1)],
}

def successor(state):
    return TREE.get(state, [])


def _ancestors(link):
    while link is not None:
        state, link = link
        yield state


def _path(link):
    return list(reversed(list(_ancestors(link))))


def ucs(s, successor, g):
    frontier = [(0, s)]
    costs = {s: 0}
    parents = {s: (s, None)}
    
    while frontier:
        cost, state = heappop(frontier)
        
        if cost != costs[state]:
            continue
        
        if state == g:
            return _path(parents[state])
        
        for next_state, step_cost in successor(state):
            new_cost = cost + step_cost
            
            if new_cost < costs.get(next_state, float("inf")):
                costs[next_state] = new_cost
                parents[next_state] = (next_state, parents[state])
                heappush(frontier, (new_cost, next_state))
                
    return None


print(ucs("S", successor, "G"))