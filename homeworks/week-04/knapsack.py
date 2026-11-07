import os
import sys
import time

import numpy as np


def plan(n):
    if n <= 500:
        return 80, 300
    if n <= 2000:
        return 60, 120
    return 40, 40


def repair(selected, weights, capacity, top_up=True):
    taken = np.cumsum(selected * weights, axis=1)
    selected &= taken <= capacity

    if not top_up:
        return selected

    room = capacity - (selected * weights).sum(axis=1)
    free = ~selected
    extra = np.cumsum(free * weights, axis=1)
    selected |= free & (extra <= room[:, None])

    return selected


def evolve(weights, values, capacity, rng):
    n = len(weights)
    size, generations = plan(n)
    rate = 1.0 / n
    elites = 2
    spots = np.arange(size)

    population = rng.random((size, n)) < 0.5
    population = repair(population, weights, capacity, top_up=False)
    history = []

    for _ in range(generations):
        scores = population @ values
        ranking = np.argsort(scores)[::-1]
        history.append(int(scores[ranking[0]]))

        left = rng.integers(0, size, size=(size, 3))
        right = rng.integers(0, size, size=(size, 3))
        mothers = left[spots, np.argmax(scores[left], axis=1)]
        fathers = right[spots, np.argmax(scores[right], axis=1)]

        mask = rng.random((size, n)) < 0.5
        children = np.where(mask, population[mothers], population[fathers])
        children ^= rng.random((size, n)) < rate
        children = repair(children, weights, capacity)
        children[:elites] = population[ranking[:elites]]

        population = children

    history.append(int((population @ values).max()))
    return history


def main():
    data = sys.stdin.read().split()
    capacity = int(data[0])
    n = int(data[1])

    numbers = np.array(data[2:2 + 2 * n], dtype=np.int64)
    weights = numbers[0::2]
    values = numbers[1::2]

    order = np.argsort(values / np.maximum(weights, 1))[::-1]
    weights = weights[order]
    values = values[order]

    started = time.perf_counter()
    history = evolve(weights, values, capacity, np.random.default_rng())
    elapsed = (time.perf_counter() - started) * 1000

    print(f"# TIMES_MS: alg={elapsed:.3f}")

    if os.environ.get("FMI_TIME_ONLY") == "1":
        return

    best = 0
    running = []
    for value in history:
        best = max(best, value)
        running.append(best)

    sys.stdout.write("\n".join(str(value) for value in running))
    sys.stdout.write(f"\n\n{best}\n")


main()