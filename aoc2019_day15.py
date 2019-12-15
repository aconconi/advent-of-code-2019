# Advent of Code 2019
# Day 15: Oxygen System

from intcomputer import IntComputer

# read input file into a list of integers
# expecting just one line of comma separated integers
with open("data/day15.dat", "r") as data_file:
    data = [int(x) for x in data_file.read().split(",")]

# Movement commands: north (1), south (2), west (3), and east (4)
NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

DIRS = [ NORTH, SOUTH, WEST, EAST]
DIRS_NAMES = { NORTH: 'N', SOUTH: 'S', WEST: 'W', EAST: 'E'}
REVERSE = {0: 0, NORTH: SOUTH, EAST: WEST, SOUTH: NORTH, WEST: EAST}

# Status codes:
WALL = 0
OK = 1
OXYGEN = 2

STATUS_CODES = { WALL, OK, OXYGEN }
STATUS_NAMES = { WALL: 'Wall', OK: 'OK', OXYGEN: 'Oxygen!'}

def adjacents(p):
    (x, y) = p
    # movement commands: north (1), south (2), west (3), and east (4)
    return [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]

def calc_adjacent(p ,d):
    if d not in DIRS: # { NORTH, EAST, SOUTH, WEST }
        raise Exception(f"Invalid direction: {d}")
    return adjacents(p)[d-1]

def move_droid(d):
    computer.append_input(d)
    computer.step(1)
    r = computer.pop_output()
    if r not in STATUS_CODES:
        raise Exception(f"Invalid status code: {r}")
    return r

# def try_droid(d):
#     r = move_droid(d)
#     if move_droid(REVERSE[d]) != OK:
#         raise Exception(f"Droid could not backtrack, something is wrong!")
#     return r

computer = IntComputer(data, [], lambda:print("mi ha chiamato"))
origin = (0, 0)
visited = set()
grid = {}
dist = {}
grid[origin] = OK
grid[0] = 0


def depth_first_recursive(v, entrance, length):
    visited.add(v)

    # explore adjacent nodes
    for d in DIRS:
        w = calc_adjacent(v, d)
        if w not in visited:
            r = move_droid(d)
            grid[w] = r
            dist[w] = length+1
            # if r == OXYGEN:
                # print(f"Oxygen found at {w} and length {length+1}!")
            if r in {OK, OXYGEN}:
                depth_first_recursive(w, d, length + 1)

    # important! the droid must also backtrack along with the search algorithm (if not at origin)
    if entrance != 0:
        move_droid(REVERSE[entrance])

# Part 1
depth_first_recursive(origin, 0, 0)
all_oxygen = [x for x in grid if grid[x] == OXYGEN]
oxygen_loc = all_oxygen[0]
print("What is the fewest number of movement commands required to move the\
repair droid from its starting position to the location of the oxygen system?")
print(dist[oxygen_loc])  # Correct answer is 424


def flood_fill(v, target, replacement, depth, max_fill_depth):
    # print(f"Visiting location {v} containing {grid[v]}")
    if target == replacement:
        return max_fill_depth
    elif grid[v] != target:
        return max_fill_depth
    else:
        # print(f"Painting location {v} from color {grid[v]} to {replacement} at depth {depth} with maxdepth {max_fill_depth}")
        grid[v] = replacement
        if depth > max_fill_depth:
            max_fill_depth = depth
    for w in adjacents(v):
        if w in grid:
            d = flood_fill(w, target, replacement, depth+1, max_fill_depth)
            if d > max_fill_depth:
                max_fill_depth = d
    return max_fill_depth

# Part 2
print("How many minutes will it take to fill with oxygen?")
grid[oxygen_loc] = OK
print(flood_fill(oxygen_loc, OK, OXYGEN, 0, 0)) # Correct answer is 446
