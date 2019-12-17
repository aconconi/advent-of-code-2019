# Advent of Code 2019
# Day 17: Set and Forget

from intcomputer import IntComputer
from collections import defaultdict

DIRS = {'^', 'v', '<', '>'}
SPACE = '.'
SCAFFOLD = '#'


def adjacents(p):
    (x, y) = p
    return [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]


# read input file into a list of integers
# expecting just one line of comma separated integers
with open("data/day17.dat", "r") as data_file:
    data = [int(x) for x in data_file.read().split(",")]

computer  = IntComputer(data, [])
computer.run()

grid = {}

x, y = 0, 0
print('01234567890123456789012345678')
for c in [chr(a) for a in computer.output_buffer]:
    if c != '\n':
        print(c, end='')
        if c != SPACE:
            grid[(x, y)] = c
        x += 1
    else:
        print("  ", y)
        y += 1
        x = 0

# Part 1
intersections = [t for t in grid if all([z in grid for z in adjacents(t)])]
print("What is the sum of the alignment parameters for the scaffold intersections?")
print(sum(x*y for (x,y) in intersections)) # Correct answer is 4112

