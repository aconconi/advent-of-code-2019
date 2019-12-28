# Advent of Code 2019
# Day 13: Care Package

from intcomputer import IntComputer

# read input file into a list of integers
# expecting just one line of comma separated integers
with open("data/day13.dat", "r") as data_file:
    data = [int(x) for x in data_file.read().split(",")]

# Tile id
EMPTY = 0
WALL = 1
BLOCK = 2
HPAD = 3
BALL = 4

# Tile rendering
TILE_ID = {EMPTY: '.', WALL: '#', BLOCK: '=', HPAD: '-', BALL: 'o'}

# Joystick
JOY_LEFT = -1
JOY_NEUTRAL = 0
JOY_RIGHT = +1


def render(screen):
    min_x = min(x for (x, y) in screen.keys())
    min_y = min(y for (x, y) in screen.keys())
    max_x = max(x for (x, y) in screen.keys())
    max_y = max(y for (x, y) in screen.keys())

    if min_x < 0 or max_x < 0 or min_y < 0 or max_y < 0:
        raise Exception(f"Negative x coordinate in screen.")

    # paint on canvas
    width = abs(max_x - min_x) + 1
    height = abs(max_y - min_y) + 1
    canvas = [[" "] * (width) for _ in range(height)]
    for (x, y), t in screen.items():
        canvas[y + abs(min_y)][x + abs(min_x)] = TILE_ID[t]

    # print canvas
    for row in canvas:
        print("".join(row))

# Part 1


def day13part1(data):
    program = data.copy()
    computer = IntComputer(program, [])
    screen = {}

    while True:
        if computer.step(3) == True:
            break
        x = computer.pop_output()
        y = computer.pop_output()
        t = computer.pop_output()
        if t not in TILE_ID:
            raise Exception(f"Invalid tile id: {t}")
        else:
            screen[(x, y)] = t

    render(screen)
    return len([t for t in screen.values() if t == BLOCK])


def day13part2(data):
    program = data.copy()
    program[0] = 2
    screen = {}
    score = 0
    ball_x = None
    pad_x = None
    joy = JOY_NEUTRAL

    computer = IntComputer(program, [JOY_NEUTRAL], lambda: joy)

    while True:
        # read from computer
        if computer.step(3) == True:
            break  # end program
        x = computer.pop_output()
        y = computer.pop_output()
        t = computer.pop_output()

        if x == -1 and y == 0:
            score = t
        else:
            screen[(x, y)] = t
            if t == BALL:
                ball_x = x
            elif t == HPAD:
                pad_x = x

        if pad_x and ball_x:
            if pad_x > ball_x:
                joy = JOY_LEFT
            elif pad_x < ball_x:
                joy = JOY_RIGHT
            else:
                joy = JOY_NEUTRAL

    render(screen)
    return score


# Part 1
print("How many block tiles are on the screen when the game exits?")
print(day13part1(data))  # Correct answer is 280

# Part 2
print("What is your score after the last block is broken?")
print(day13part2(data))  # Correct answer is 13298
