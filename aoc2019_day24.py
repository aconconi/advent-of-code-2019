# Advent of Code 2019
# Day 24: # Advent of Code 2019

from collections import defaultdict

BUG = '#'
EMPTY = '.'
SIZE = 5

grid = {}

# read input file and generate asteroids
with open("data/day24.dat", "r") as data_file:
    for y,line in enumerate(data_file):
        for x,c in enumerate(line.strip()):
            grid[(x,y)] = c


def adjacents(pos):
    x, y = pos
    return ((x+1, y), (x-1, y), (x, y-1), (x, y+1))

def num_adjacents(pos, grid):
    c = 0
    for p in adjacents(pos):
        if p in grid.keys() and grid[p] == BUG:
            c +=1
    return c
  
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
    return sum([pow(2,i) for i,p in enumerate(grid) if grid[p] == BUG])

# render(grid)
# for i in range(4):
#     grid = evolve(grid)
#     print()

#     render(grid)
#     print(hash_grid(grid))
    
counter = set()
while True:
    grid = evolve(grid)
    h = hash_grid(grid)
    if h in counter:
        break
    else:
        counter.add(h)

print("What is the biodiversity rating for the first layout that appears twice?")
print(rating(grid)) # Correct answer is 20751345