# Advent of Code 2019
# Day 21: Springdroid Adventure

from intcomputer import IntComputer

# read input file into a list of integers
# expecting just one line of comma separated integers
with open("data/day21.dat", "r") as data_file:
    data = [int(x) for x in data_file.read().split(",")]

# Part 1
script = 'NOT A J\n' \
        + 'NOT B T\n' \
        + 'OR T J\n'  \
        + 'NOT C T\n' \
        + 'OR T J\n'  \
        + 'AND D J\n' \
        + 'WALK\n'
computer = IntComputer(data, [ord(c) for c in script])
computer.run()
render = "".join([chr(c) for c in computer.output_buffer[:-1]])
print("What amount of hull damage does it report?")
print(computer.output_buffer[-1:][0])

# Part 2
print("Successfully survey the rest of the hull by ending your program with RUN.")
print("What amount of hull damage does the springdroid now report?")
script = 'NOT C J\n' \
        + 'AND H J\n' \
        + 'NOT B T\n' \
        + 'OR T J\n'  \
        + 'NOT A T\n' \
        + 'OR T J\n'  \
        + 'AND D J\n' \
        + 'RUN\n'
computer.__init__(data, [ord(c) for c in script])
computer.run()
print(computer.output_buffer[-1:][0])
