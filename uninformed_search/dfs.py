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


def dfs(s, successor, g):
    frontier = [s]
    parents = [None]
    
    while frontier:
        state = frontier.pop()
        link = (state, parents.pop())
        
        if state == g:
            return _path(link)
        
        for next_state, _ in reversed(successor(state)):
            frontier.append(next_state)
            parents.append(link)
        
    return None

print(dfs("S", successor, "G1"))