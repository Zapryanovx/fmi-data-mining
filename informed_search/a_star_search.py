from heapq import heappop, heappush, nsmallest
from itertools import count

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


def astar(s, successor, g, h):
    order = count()
    frontier = [(h(s), next(order), s)]
    costs = {s: 0}
    parents = {s: (s, None)}
    
    while frontier:
        f, _, state = heappop(frontier)
        
        if f != costs[state] + h(state):
            continue
        
        if state == g:
            return _path(parents[state])
        
        for next_state, step_cost in successor(state):
            new_cost = costs[state] + step_cost
            
            if new_cost < costs.get(next_state, float("inf")):
                costs[next_state] = new_cost
                parents[next_state] = (next_state, parents[state])
                heappush(frontier, (new_cost + h(next_state), next(order), next_state))
                
    return None


print(astar("S", successor, "G", heuristic))