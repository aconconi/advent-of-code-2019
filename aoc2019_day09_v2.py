# Advent of Code 2019
# Day 9: Sensor Boost

from intcomputer import IntComputer

# read input file into a list of integers
# expecting just one line of comma separated integers
with open("data/day09.dat", "r") as data_file:
    data = [int(x) for x in data_file.read().split(",")]


def day09part1(program):
    computer = IntComputer(program.copy(), [1])
    computer.run()
    return computer.output_buffer


def day09part2(program):
    computer = IntComputer(program.copy(), [2])
    computer.run()
    return computer.output_buffer


# Test cases for Part 1
test_program1 = [109, 1, 204, -1, 1001, 100, 1,
                 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
test_program2 = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
test_program3 = [104, 1125899906842624, 99]

assert day09part1(test_program1) == test_program1
assert len(str(day09part1(test_program2)[0])) == 16
assert day09part1(test_program3) == [1125899906842624]

# # Part 1
print("What BOOST keycode does it produce?")
print(day09part1(data))  # Correct answer is 3765554916

# # print(day09part1([9,4, 204,0, 99], [1000]))
print("What are the coordinates of the distress signal?")
print(day09part2(data))  # Correct answer is 76642

# # Part 2
# print("In feedback loop mode, what is the highest signal that can be sent to the thrusters?")
# print(day07part2(data)) # Correct answer is
