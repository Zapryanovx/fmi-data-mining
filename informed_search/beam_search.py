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


def beam(s, successor, g, h, l):
    order = count()
    frontier = [(h(s), next(order), s)]
    parents = {s: (s, None)}
    
    while frontier:
        _, _, state = heappop(frontier)
        
        if state == g:
            return _path(parents[state])
        
        for next_state, _ in successor(state):
            if next_state not in parents:
                parents[next_state] = (next_state, parents[state])
                heappush(frontier, (h(next_state), next(order), next_state))
                
        frontier = nsmallest(l, frontier)   

    return None


print(beam("S", successor, "G", heuristic, 2))