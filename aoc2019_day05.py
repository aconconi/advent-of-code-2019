# Advent of Code 2019
# Day 3: Sunny with a Chance of Asteroids

import operator

# read input file into a list of integers
# expecting just one line of comma separated integers
with open("data/day05.dat", "r") as data_file:
    data = [int(x) for x in data_file.read().split(",")]

def run_program(memory, input_value):

    out = []
    m = memory.copy()

    # instruction pointer
    x = 0
    full_opcode = ""

    # get value by dereferencing pointer if needed
    def deref(mode, val):
        # '1' is immediate mode, '0' is position mode
        return val if mode == '1' else m[val]

    def deref_par(i):
        return deref(full_opcode[3-i], m[x+i])

    def read_par(i):
        return m[x+i]

    while m[x] != 99:
        full_opcode = str(m[x]).zfill(5)  # pad string with 0 so that it's always 5 digits
        opcode = int(full_opcode[3:])     # opcode is two rightmost digits
        if opcode in [1,2]:
            # Sum or Multiply
            a, b, c = deref_par(1), deref_par(2), read_par(3)
            m[c] = a + b if opcode == 1 else a * b
            x += 4
        elif opcode == 3:
            # Operation: input
            a = read_par(1)
            m[a] = input_value
            x += 2
        elif opcode == 4:
            # Operation: output
            a = deref_par(1)
            out.append(a)  
            x += 2
        elif opcode == 5:
            # Operation: jump-if-true
            a, b = deref_par(1), deref_par(2)
            x = b if a != 0 else x+3
        elif opcode == 6:
            # Operation: jump-if-false
            a, b = deref_par(1), deref_par(2)
            x = b if a == 0 else x+3
        elif opcode == 7:
            # Operation: less-than
            a, b, c = deref_par(1), deref_par(2), read_par(3)
            m[c] = 1 if a < b else 0
            x += 4
        elif opcode == 8:
            # Operation: less-than
            a, b, c = deref_par(1), deref_par(2), read_par(3)
            m[c] = 1 if a == b else 0
            x += 4           
        else:
            print("Invalid opcode found.")
            exit(1)
    return out

# Part 1
def day05part1(data):
    return run_program(data, 1)[-1]
    

# Part 2
def day05part2(data):
    return run_program(data, 5)[-1]

# Part 1
print("After providing 1 to the only input instruction and passing all \
the tests, what diagnostic code does the program produce?")
print(day05part1(data)) # Correct answer is 3122865

# Part 2
print("What is the diagnostic code for system ID 5?")
print(day05part2(data)) # Correct answer is 773660


