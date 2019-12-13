# Advent of Code 2019
# Day 11: Sensor Boost

from collections import defaultdict, deque
from intcomputer import IntComputer

WHITE = 1
BLACK = 0

INC = { 'UP':    (0, -1),
        'DOWN':  (0, +1),
        'RIGHT': (+1, 0),
        'LEFT':  (-1, 0)          
}

def paint(program, start_col):
    rx, ry = 0, 0
    direction = deque(['UP', 'LEFT', 'DOWN', 'RIGHT'])
    panels = defaultdict(lambda: BLACK)

    panels[(rx,ry)] = start_col
    computer = IntComputer(program, [])

    while True:
        # send camera data to computer inputs
        computer.append_input( panels[(rx,ry)] )
            
        # get color from computer output
        if computer.step() == True:
            break
        panels[(rx,ry)] = computer.pop_output()

        # get rotation from computer output
        if computer.step() == True:
            break
        
        # rotate
        rot = computer.pop_output()
        if rot == 1:
            # turn right
            direction.rotate(+1) 
        elif rot == 0:
            # turn left
            direction.rotate(-1)
        else:
            raise Exception(f"Invalid rotation: {rot}")

        # step forward
        rx += INC[direction[0]][0]
        ry += INC[direction[0]][1]
       
    return panels

def day11part1(data):
    return len(paint(data, BLACK))

# def day11part2(data):
#     image = paint(data, WHITE)
#     min_width = min(map(lambda x: x[0], image.keys()))
#     min_height = min(map(lambda x: x[1], image.keys()))
#     image = { (x - min_width, y - min_height): v for (x, y), v in image.items()}
#     width = max(map(lambda x: x[0], image.keys())) + 1
#     height = max(map(lambda x: x[1], image.keys())) + 1
#     output = [[" "] * width for _ in range(height)]
#     for (x, y), v in image.items():
#         if v == 1:
#             output[y][x] = "#"
#     for row in output:
#         print("".join(row))

def day11part2(data):
    panels = paint(data, WHITE)

    # get extremes
    min_x = min(x for (x,y) in panels.keys())
    min_y = min(y for (x,y) in panels.keys())
    max_x = max(x for (x,y) in panels.keys())
    max_y = max(y for (x,y) in panels.keys())
 
    # shift panel coordinates and retain only white panels
    panels = { (x - min_x, y - min_y) : col for (x, y), col in panels.items() if col == WHITE}
 
    # paint on canvas
    width =  abs(max_x - min_x) + 1
    height = abs(max_y - min_y) + 1
    canvas = [[" "] * (width) for _ in range(height)]
    for (x, y),_ in panels.items():
        canvas[y + abs(min_y)][x + abs(min_x)] = "\u2588"

    # print canvas
    for row in canvas:
        print("".join(row))


# read input file into a list of integers
# expecting just one line of comma separated integers
with open("data/day11.dat", "r") as data_file:
    data = [int(x) for x in data_file.read().split(",")]

# Part 1
print("How many panels does it paint at least once?")
print(day11part1(data)) # Correct answer is 1686

# Part 2
print("After starting the robot on a single white panel instead, what registration identifier does it paint on your hull?")
day11part2(data) # Correct answer is GARPKZUL

