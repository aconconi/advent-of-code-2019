# Advent of Code 2019
# Day 17: Set and Forget

from intcomputer import IntComputer
from collections import defaultdict

ROBOT_DIRS = {'^', 'v', '<', '>'}
SPACE = '.'
SCAFFOLD = '#'

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


# read input file into a list of integers
# expecting just one line of comma separated integers
with open("data/day17.dat", "r") as data_file:
    data = [int(x) for x in data_file.read().split(",")]

computer  = IntComputer(data, [])
computer.run()

grid = {}
x, y = 0, 0
robot_loc = None
robot_dir = None
for c in [chr(a) for a in computer.output_buffer]:
    if c != '\n':
        print(c, end='')
        if c != SPACE:
            grid[(x, y)] = '#'
            if c in ROBOT_DIRS:
                (rx, ry) =  (x, y)
                robot_dir = c
        x += 1
    else:
        y += 1
        x = 0
        print()

# Part 1
intersections = [t for t in grid if all([z in grid for z in adjacents(t)])]
print("What is the sum of the alignment parameters for the scaffold intersections?")
print(sum(x*y for (x,y) in intersections)) # Correct answer is 4112


def encode(s):
    r = []
    for c in s:
        for c2 in c:
            r.append(ord(c2))
        r.append(44)
    r[-1] = 10
    return r

# Some test cases for encode function
assert encode(['A','B','C','B','A','C']) == [65, 44, 66, 44, 67, 44, 66, 44, 65, 44, 67, 10]
assert encode(['R','8','R','8']) == [82, 44, 56, 44, 82, 44, 56, 10]
assert encode(['R','4','R','4','R','8']) == [82, 44, 52, 44, 82, 44, 52, 44, 82, 44, 56, 10]
assert encode(['L','6','L','2']) == [76, 44, 54, 44, 76, 44, 50, 10]

# Part 2
assert data[0] == 1
data[0] = 2
computer  = IntComputer(data, [])
seq_main = encode(['A','B','A','C','A','B','C','B','C','B'])
seq_a = encode(['R','10','R','10','R','6', 'R','4'])
seq_b = encode(['R','10','R','10','L','4'])
seq_c = encode(['R','4','L','4','L','10', 'L','10'])
computer.input_buffer = seq_main + seq_a + seq_b + seq_c + encode('n')
computer.run()
print("After visiting every part of the scaffold at least once, how much dust does the vacuum robot report it has collected?")
print(computer.output_buffer[-1]) # Correct answer is 578918

# def suffix_tree(s):
#     st = set()
#     for i in enumerate(s):
#         s.add(s[-i:])
    