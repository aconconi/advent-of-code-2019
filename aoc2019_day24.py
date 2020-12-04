# Advent of Code 2019
# Day 24: # Advent of Code 2019

from collections import defaultdict

BUG = '#'
EMPTY = '.'
SIZE = 5

data = {}

# read input file and generate asteroids
with open("data/day24.dat", "r") as data_file:
    for y, line in enumerate(data_file):
        for x, c in enumerate(line.strip()):
            data[(x, y)] = c


def adjacents(pos):
    x, y = pos
    return ((a, b) for (a, b) in {(x+1, y), (x-1, y), (x, y-1), (x, y+1)} if 0 <= a < SIZE and 0 <= b < SIZE)


def num_adjacents(pos, grid):
    return [grid[p] for p in adjacents(pos)].count(BUG)


def render(grid):
    for i, p in enumerate(grid):
        print(grid[p], end='')
        if not (i+1) % SIZE:
            print()


def evolve(grid):
    new = grid.copy()
    for p in new:
        # print(f"assessing {p}")
        if grid[p] == BUG:
            if num_adjacents(p, grid) != 1:
                # A bug dies (becoming an empty space) unless there is exactly one bug adjacent to it.
                new[p] = EMPTY
        else:
            # An empty space becomes infested with a bug if exactly one or two bugs are adjacent to it.
            if 1 <= num_adjacents(p, grid) <= 2:
                new[p] = BUG
    return new


def hash_grid(grid):
    return "".join(c for c in grid.values())


def rating(grid):
    return sum(pow(2, i) for i, p in enumerate(grid) if grid[p] == BUG)


def day24part1(data):
    grid = data.copy()
    counter = set()
    while True:
        grid = evolve(grid)
        h = hash_grid(grid)
        if h in counter:
            break
        else:
            counter.add(h)
    return rating(grid)


def num_adjacents2(pos, world):
    x, y, z = pos
    ans = 0

    if (x, y) == (2, 2):
        return 0

    # count on same level
    adjacents2 = ((a, b, c) for (a, b, c) in {(x+1, y, z), (x-1, y, z), (x, y-1, z), (x, y+1, z)}
                  if 0 <= a < SIZE and 0 <= b < SIZE and (a, b) != (2, 2))
    ans += [world[x2, y2, z2] for x2, y2, z2 in adjacents2].count(BUG)

    # count on inner level
    if (x, y) == (2, 1):
        ans += [world[(x2, 0, z+1)] for x2 in range(5)].count(BUG)
    elif (x, y) == (2, 3):
        ans += [world[(x2, 4, z+1)] for x2 in range(5)].count(BUG)
    elif (x, y) == (1, 2):
        ans += [world[(0, y2, z+1)] for y2 in range(5)].count(BUG)
    elif (x, y) == (3, 2):
        ans += [world[(4, y2, z+1)] for y2 in range(5)].count(BUG)

    # count on outer level
    if (x, y, z) in [(x2, 0, z) for x2 in range(5)]:
        ans += 1 if world[(2, 1, z-1)] == BUG else 0
    if (x, y, z) in [(x2, 4, z) for x2 in range(5)]:
        ans += 1 if world[(2, 3, z-1)] == BUG else 0
    if (x, y, z) in [(0, y2, z) for y2 in range(5)]:
        ans += 1 if world[(1, 2, z-1)] == BUG else 0
    if (x, y, z) in [(4, y2, z) for y2 in range(5)]:
        ans += 1 if world[(3, 2, z-1)] == BUG else 0

    return ans


def evolve2(grid):
    new = grid.copy()

    # pad levels if necessary
    min_level = min(z for (_, _, z) in grid)
    max_level = max(z for (_, _, z) in grid)
    # print(f"min {min_level}  max {max_level}")

    if [grid[(x, y, min_level)] for x in range(5) for y in range(5)].count(BUG):
        for x in range(SIZE):
            for y in range(SIZE):
                new[(x, y, min_level-1)] == EMPTY
    if [grid[(x, y, max_level)] for x in range(5) for y in range(5)].count(BUG):
        for x in range(SIZE):
            for y in range(SIZE):
                new[(x, y, max_level+1)] == EMPTY

    for p in new:
        # print(f"assessing {p}")
        if grid[p] == BUG:
            if num_adjacents2(p, grid) != 1:
                # A bug dies (becoming an empty space) unless there is exactly one bug adjacent to it.
                new[p] = EMPTY
        else:
            # An empty space becomes infested with a bug if exactly one or two bugs are adjacent to it.
            if 1 <= num_adjacents2(p, grid) <= 2:
                new[p] = BUG
    return new


def day24part2(data, iterations):
    grid = defaultdict(lambda: EMPTY)

    for p in data:
        (x, y) = p
        grid[(x, y, 0)] = data[p]

    for _ in range(iterations):
        grid = evolve2(grid)

    return [grid[p] for p in grid].count(BUG)


# Part 1
print("What is the biodiversity rating for the first layout that appears twice?")
print(day24part1(data))  # Correct answer is 20751345


# Part 2
print("How many bugs are present after 200 minutes?")
print(day24part2(data, 200))  # Correct answer is 1983
