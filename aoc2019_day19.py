# Advent of Code 2019
# Day 19: Tractor Beam

from intcomputer import IntComputer

# read input file into a list of integers
# expecting just one line of comma separated integers
with open("data/day19.dat", "r") as data_file:
    data = [int(x) for x in data_file.read().split(",")]


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
    for r, row in enumerate(canvas):
        print("".join(row), r)
    for j in range(width):
        if j % 10 == 0:
            print(str(j // 10)  + ' ' * 9, end='')
    print()   
    for j in range(width):
        print(j % 10, end='')
    print()
 
def probe(x, y):
    computer.__init__(data, [x, y])
    computer.run()
    return computer.pop_output()


def day19part1(data):
    grid = {}
    c = 0
    for x in range(0,50):
        for y in range(0,50):
            t = probe(x, y)
            c += t
            grid[x, y] = '#' if t == 1 else '.'
    render(grid)
    return c


def day19part2(data):
    # start point manually defined looking at the rendering from part 1
    x, y = 42, 49
    
    while True:
        # track left side of beam
        while not probe(x,y):
            x += 1
        if probe(x + 99, y - 99):
            # opposite vertex of square is within the beam, solution found
            break
        else:
            y += 1
        
    return(x * 10000 + (y-99))


computer  = IntComputer(data)

# Part 1
print("How many points are affected by the tractor beam in the 50x50 area closest to the emitter?")
print(day19part1(data)) # Correct answer is 112

# Part 2
print("What value do you get if you take that point's X coordinate, multiply it by 10000, then add the point's Y coordinate?")
print(day19part2(data)) # Correct answer is 18261982