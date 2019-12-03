# Advent of Code 2019
# Day 3: Crossed Wires

from collections.abc import Set

# read input file into an array of integers
# expecting just one line of comma separated integers
data = []
with open("data/day03.dat", "r") as data_file:
    for line in data_file.read().splitlines():
        data.append(line)

# taxicab aka Manhattan distance
def taxicab_distance(x1, y1,x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)

# generates a list of all locations visited by the wire (including repetitions)
# input: wire as string
# output: path as list of (x,y) 
def path(wire):
    result = []
    (x, y) = (0, 0)
    INC = { "L": (-1, 0), "R": (+1, 0), "U": (0, +1), "D": (0, -1) }
    for stretch in wire.split(","):
        for _ in range(int(stretch[1:])):
            x += INC[stretch[0]][0]
            y += INC[stretch[0]][1]
            result += [(x,y)]
    return result

# def path_length(path, loc):
#    return path.index(loc) + 1  

# def nearest_intersection(a,b):
#    return min(set(path(a)) & set(path(b)), key=lambda z: taxicab_distance(0,0, z[0], z[1]))

def day03part1(a, b):
   return min( taxicab_distance(0, 0, z[0], z[1]) for z in set(path(a)) & set(path(b)) )

# Some test cases for Part 1
assert day03part1("R8,U5,L5,D3", "U7,R6,D4,L4") == 6
assert day03part1("R75,D30,R83,U83,L12,D49,R71,U7,L72", \
                  "U62,R66,U55,R34,D71,R55,D58,R83") == 159
assert day03part1("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", \
                  "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7") ==  135

# Part 2
def day03part2(a, b):
    pa = path(a)
    pb = path(b)  
    return min( pa.index(z) + pb.index(z) + 2 for z in set(pa) & set(pb) )

# Some test cases for Part 2
assert day03part2("R8,U5,L5,D3", "U7,R6,D4,L4") == 30
assert day03part2("R75,D30,R83,U83,L12,D49,R71,U7,L72", \
                  "U62,R66,U55,R34,D71,R55,D58,R83") == 610
assert day03part2("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", \
                  "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7") ==  410

# Part 1
print("What is the Manhattan distance from the central port to the closest intersection")
print(day03part1(data[0], data[1])) # Answer is 651

# Part 2
print("What is the fewest combined steps the wires must take to reach an intersection?")
print(day03part2(data[0], data[1])) # Answer is 7534