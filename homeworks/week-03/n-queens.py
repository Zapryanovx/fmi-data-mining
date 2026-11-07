import os
import random
import sys
import time

TRIES = 64


def attempt(n, rng):
    randrange = rng.randrange
    size = 2 * n - 1

    rows = [0] * n
    pos = [0] * size
    neg = [0] * size

    queens = list(range(n))
    rng.shuffle(queens)

    for c in range(n):
        for _ in range(TRIES):
            k = randrange(c, n)
            r = queens[k]
            if not pos[r + c] and not neg[n - 1 - r + c]:
                queens[c], queens[k] = queens[k], queens[c]
                break

        r = queens[c]
        rows[r] += 1
        pos[r + c] += 1
        neg[n - 1 - r + c] += 1

    ties = []

    for _ in range(2 * n + 200):
        conflicted = [c for c in range(n)
                      if rows[queens[c]] + pos[queens[c] + c] + neg[n - 1 - queens[c] + c] > 3]

        if not conflicted:
            return queens

        c = conflicted[randrange(len(conflicted))]
        r = queens[c]

        rows[r] -= 1
        pos[r + c] -= 1
        neg[n - 1 - r + c] -= 1

        best = n + 1
        ties.clear()
        base = n - 1 + c

        for k in range(n):
            value = rows[k] + pos[k + c] + neg[base - k]

            if value < best:
                best = value
                ties.clear()
                ties.append(k)
            elif value == best:
                ties.append(k)

        r = ties[randrange(len(ties))]
        queens[c] = r

        rows[r] += 1
        pos[r + c] += 1
        neg[n - 1 - r + c] += 1

    return None


def solve(n):
    if n == 1:
        return [0]
    if n in (2, 3):
        return None

    rng = random.Random()

    while True:
        queens = attempt(n, rng)
        if queens is not None:
            return queens


def board(queens):
    n = len(queens)
    where = [0] * n

    for c, r in enumerate(queens):
        where[r] = c

    return "\n".join(" ".join("*" if where[r] == c else "_" for c in range(n))
                     for r in range(n))


def main():
    n = int(sys.stdin.readline())

    started = time.perf_counter()
    queens = solve(n)
    elapsed = (time.perf_counter() - started) * 1000

    print(f"# TIMES_MS: alg={elapsed:.3f}")

    if os.environ.get("FMI_TIME_ONLY") == "1":
        return

    if queens is None:
        print(-1)
        return

    if "--board" in sys.argv:
        print(board(queens))
    else:
        print(queens)


main()