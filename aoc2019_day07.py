# Advent of Code 2019
# Day 7: Amplification Circuit

from itertools import permutations

# read input file into a list of integers
# expecting just one line of comma separated integers
with open("data/day07.dat", "r") as data_file:
    data = [int(x) for x in data_file.read().split(",")]


def run_program(m, input_values):
    out = []
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
            # Operation: sum or multiply
            a, b, c = deref_par(1), deref_par(2), read_par(3)
            m[c] = a + b if opcode == 1 else a * b
            x += 4
        elif opcode == 3:
            # Operation: input
            a = read_par(1)
            m[a] = input_values.pop(0)
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


def thruster_signal(program, phases):
    r = 0
    for f in phases:
        r = run_program(program.copy(), [f, r]).pop()
    return r

def feedback_loop(program, phases):
    # set up the memory space for each amplifier by cloning the program
    mem  = [program for _ in phases]
    return mem
    

def day07part1(program):
    return max([thruster_signal(program, phases) for phases in permutations([0,1,2,3,4])])

# Some test cases
test_program1 = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
assert thruster_signal(test_program1, [4,3,2,1,0]) == 43210
assert day07part1(test_program1) == 43210

test_program2 = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,\
23,1,24,23,23,4,23,99,0,0]
assert thruster_signal(test_program2, [0,1,2,3,4]) == 54321
assert day07part1(test_program2) == 54321

test_program3 = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,\
1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
assert thruster_signal(test_program3, [1,0,4,3,2]) == 65210
assert day07part1(test_program3) == 65210




# Part 1
print("What is the highest signal that can be sent to the thrusters?")
print(day07part1(data)) # Correct answer is 359142