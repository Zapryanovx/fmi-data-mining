CYCLE = {
    "S": [("A", 1)],
    "A": [("S", 1), ("G", 1)],
}


def cycle_successor(state):
    return CYCLE.get(state, [])


def _ancestors(link):
    while link is not None:
        state, link = link
        yield state


def _path(link):
    return list(reversed(list(_ancestors(link))))


def _dls(s, successor, g, limit):
    frontier = [s]
    metadata = [(None, limit)]
    cutoff = False
    
    while frontier:
        state = frontier.pop()
        parent, remaining = metadata.pop()
        link = (state, parent)
        
        if state == g:
            return _path(link), False
        
        if remaining == 0:
            cutoff = True
            continue
        
        for next_state, _ in reversed(successor(state)):
            if next_state not in _ancestors(link):
                frontier.append(next_state)
                metadata.append((link, remaining - 1))
                
    return None, cutoff


def ids(s, successor, g):
    limit = 0
    
    while True:
        path, cutoff = _dls(s, successor, g, limit)
        
        if path is not None:
            return path
        if not cutoff:
            return None
            
        limit += 1    
    

print(ids("S", cycle_successor, "G")) 

