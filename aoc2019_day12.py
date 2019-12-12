# Advent of Code 2019
# Day 12: The N-Body Problem

from itertools import permutations
import operator
from math import gcd

# read input file and generate asteroids
data = []
with open("data/day12.dat", "r") as data_file:
    for line in data_file.read().splitlines():
        line = ''.join([c for c in line if c not in '<>xyz='])
        (x,y,z) = ( int(c) for c in line.split(',') ) 
        data.append((x,y,z))

# <x=-1, y=0, z=2>
# <x=2, y=-10, z=-7>
# <x=4, y=-8, z=8>
# <x=3, y=5, z=-1>
testdata1 = [ (-1,0,2), (2,-10,-7), (4,-8,8), (3,5,-1) ]

# <x=-8, y=-10, z=0>
# <x=5, y=5, z=10>
# <x=2, y=-7, z=3>
# <x=9, y=-8, z=-3>
testdata2 = [ (-8,-10,0), (5,5,10), (2,-7,3), (9,-8,-3)]

class Moon():
    def __init__(self, pos):
        self.pos = pos
        self.vel = (0,0,0)
    
    def __repr__(self):
        return("pos=" + str(self.pos) + ", vel=" + str(self.vel))
    
    def apply_velocity(self):
        self.pos = tuple(map(operator.add, self.pos, self.vel))
    
    def pull_vector(self, other):
            return tuple( map(lambda s,o: (o-s) // abs(o-s) if abs(o-s) else 0, self.pos, other.pos))
        
    def apply_gravity(self, other):
        # map(operator.add, self.vel, self.pull_vector(other))
        def pull(s, o):
            return (o-s) // abs(o-s) if abs(o-s) else 0

        (x, y, z) = self.pos 
        (other_x, other_y, other_z) = other.pos
        (vx, vy, vz) = self.vel
        self.vel = (vx + pull(x, other_x),
                    vy + pull(y, other_y),
                    vz + pull(z, other_z))
        
    def pot_energy(self):
        return sum(abs(comp) for comp in self.pos)
    
    def kin_energy(self):
        return sum(abs(comp) for comp in self.vel)
    
    def tot_energy(self):
        return self.pot_energy() * self.kin_energy() 

    def offset(self, other):
        return tuple(map(operator.sub, self.pos, other.pos))

def lcm(a, b):
    return abs(a*b) // gcd(a, b)


def tick(moons):
    # apply gravity
    for (a,b) in permutations(moons, 2):
        a.apply_gravity(b)
    
    # apply velocity
    for m in moons:
        m.apply_velocity()


def day12part1(positions, steps):
    moons = [Moon(p) for p in positions]
    for _ in range(steps):
        tick(moons)        
    return sum(m.tot_energy() for m in moons)


def day12part2(positions):
    # create moons from list of positions
    moons = [Moon(p) for p in positions]

    # write down initial positions
    initial_mem = [(m.pos, m.vel) for m in moons]    
    initial_x = [(x, vx) for ((x,_,_), (vx,_,_)) in initial_mem]
    initial_y = [(y, vy) for ((_,y,_), (_,vy,_)) in initial_mem]
    initial_z = [(z, vz) for ((_,_,z), (_,_,vz)) in initial_mem]
    sx, sy, sz = None, None, None

    # simulate
    i = 0
    while True:
        tick(moons)
        i += 1
        mem = [(m.pos, m.vel) for m in moons]
        if [(x, vx) for ((x,_,_), (vx,_,_)) in mem] == initial_x and not sx:
            sx = i
        if [(y, vy) for ((_,y,_), (_,vy,_)) in mem] == initial_y and not sy:
            sy = i
        if [(z, vz) for ((_,_,z), (_,_,vz)) in mem] == initial_z and not sz:
            sz = i

        if sx and sy and sz:
            return lcm(lcm(sx, sy), sz)

# Some test cases
assert day12part1(testdata1, 10) == 179
assert day12part1(testdata2, 100) == 1940  
assert day12part2(testdata1) == 2772
assert day12part2(testdata2) == 4686774924

# Part 1
print("What is the total energy in the system after simulating the moons?")
print(day12part1(data, 1000)) # Correct answer is 10028         

print("How many steps does it take to reach the first state that exactly matches a previous state?")
print(day12part2(testdata2)) # Correct answer is 314610635824376

