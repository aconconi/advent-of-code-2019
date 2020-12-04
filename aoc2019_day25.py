# Advent of Code 2019
# Day 25: Cryostasis

from intcomputer import IntComputer


# read input file into a list of integers
# expecting just one line of comma separated integers
with open("data/day25.dat", "r") as data_file:
    data = [int(x) for x in data_file.read().split(",")]


def provide_input():
    command = input()
    for c in command:
        computer.append_input(ord(c))
    return ord('\n')


computer = IntComputer(data, [], provide_input)
while True:
    terminated = computer.step_until_output()
    if computer.output_buffer:
        print(chr(computer.pop_output()), end='')
    if terminated:
        print("Program halted.")
        break

# Played manually, got past the sensor with this set of items:
# - food ration
# - fixed point
# - semiconductor
# - planetoid

# "Oh, hello! You should be able to get in by typing 34095120
# on the keypad at the main airlock."
