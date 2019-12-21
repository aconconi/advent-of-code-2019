# Advent of Code 2019
# Day 19: Tractor Beam

from intcomputer import IntComputer
from collections import defaultdict
from itertools import combinations 


NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

DIRS = [ NORTH, SOUTH, WEST, EAST]
DIRS_NAMES = { NORTH: 'N', SOUTH: 'S', WEST: 'W', EAST: 'E'}
REVERSE = {0: 0, NORTH: SOUTH, EAST: WEST, SOUTH: NORTH, WEST: EAST}


def adjacents(p):
    (x, y) = p
    return [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]

def render(screen):
    min_x = min(x for (x,y) in screen.keys())
    min_y = min(y for (x,y) in screen.keys())
    max_x = max(x for (x,y) in screen.keys())
    max_y = max(y for (x,y) in screen.keys())
    
    if min_x < 0 or max_x < 0 or min_y < 0 or max_y < 0:
        raise Exception(f"Negative x coordinate in screen.")
 
    # paint on canvas
    width =  abs(max_x - min_x) + 1
    height = abs(max_y - min_y) + 1
    canvas = [[" "] * (width) for _ in range(height)]
    for (x, y),t in screen.items():
        canvas[y - abs(min_y)][x - abs(min_x)] = t

    # print canvas
    for row in canvas:
        print("".join(row))

# read input file into a list of integers
# expecting just one line of comma separated integers
with open("data/day19.dat", "r") as data_file:
    data = [int(x) for x in data_file.read().split(",")]

grid = {}
computer  = IntComputer(data, [])
c = 0
for x in range(0,50):
    for y in range(0,50):
        computer  = IntComputer(data, [x, y])
        computer.run()
        t = computer.pop_output()
        c += t
        grid[x, y] = '#' if t == 1 else '.'

render(grid)
print(c)