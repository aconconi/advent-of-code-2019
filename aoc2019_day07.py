# Advent of Code 2019
# Day 7: Amplification Circuit

from itertools import permutations, cycle
from collections import deque

class IntComputer():
    def __init__(self, program, input_values):
        self.mem = program.copy()
        self.input_buffer = input_values
        self.pc = 0
        self.output_buffer = []
        self.stepping = False
        self.command = ""

    def append_input(self, val):
        self.input_buffer.append(val)

    def pop_output(self):
        return self.output_buffer.pop(0) if self.output_buffer else None

    def step(self):
        self.stepping = True
        return self.run()

    def run(self):
        # get value by dereferencing pointer if needed
        def deref(mode, val):
            # '1' is immediate mode, '0' is position mode
            return val if mode == '1' else self.mem[val]

        def deref_par(i):
            return deref(self.command[3-i], self.mem[self.pc+i])

        def read_par(i):
            return self.mem[self.pc+i]

        def write_mem(loc, val):
            self.mem[loc] = val

        while self.mem[self.pc] != 99:
            self.command = str(self.mem[self.pc]).zfill(5)  # pad string with 0 so that it's always 5 digits
            opcode = int(self.command[3:])     # opcode is two rightmost digits
            if opcode in [1,2]:
                # Operation: sum or multiply
                a, b, c = deref_par(1), deref_par(2), read_par(3)
                write_mem(c, a + b if opcode == 1 else a * b)
                self.pc += 4
            elif opcode == 3:
                # Operation: input
                write_mem(read_par(1), self.input_buffer.pop(0))
                self.pc += 2
            elif opcode == 4:
                # Operation: output
                a = deref_par(1)
                self.output_buffer.append(a)  
                self.pc += 2
                # if stepping, give back control after output
                if self.stepping:
                    return False
            elif opcode == 5:
                # Operation: jump-if-true
                a, b = deref_par(1), deref_par(2)
                self.pc = b if a != 0 else self.pc+3
            elif opcode == 6:
                # Operation: jump-if-false
                a, b = deref_par(1), deref_par(2)
                self.pc = b if a == 0 else self.pc+3
            elif opcode == 7:
                # Operation: less-than
                a, b, c = deref_par(1), deref_par(2), read_par(3)
                write_mem(c, 1 if a < b else 0)
                self.pc += 4
            elif opcode == 8:
                # Operation: less-than
                a, b, c = deref_par(1), deref_par(2), read_par(3)
                write_mem(c, 1 if a == b else 0)
                self.pc += 4           
            else:
                print("Invalid opcode found.")
                exit(1)

        return True


# read input file into a list of integers
# expecting just one line of comma separated integers
with open("data/day07.dat", "r") as data_file:
    data = [int(x) for x in data_file.read().split(",")]


def thruster_signal(program, phases):
    r = 0
    for f in phases:
        amp = IntComputer(program.copy(), [f, r])
        amp.run()
        r = amp.pop_output()
    return r

def feedback_loop(program, phases):
    # set up context for each amplifier 
    amps = [ IntComputer(program, [f]) for f in phases]
    signal = 0
    for i,a in cycle(enumerate(amps)):
        if signal != None:
            a.append_input(signal)
        
        # print("-> amp i:",i," pc:", a.pc, " in:", a.input_buffer, " out:", a.output_buffer, "fo:", a.command)
        
        if a.input_buffer:
            a.step()
            # print("<- amp i:",i," pc:", a.pc, " in:", a.input_buffer, " out:", a.output_buffer, "fo:", a.command)
            # program paused after output
            new_signal = a.pop_output()

            if new_signal:
                signal = new_signal
            else:
                return signal


def day07part1(program):
    return max([thruster_signal(program, phases) for phases in permutations([0,1,2,3,4])])

def day07part2(program):
    return max([feedback_loop(program, phases) for phases in permutations([5,6,7,8,9])])


# Test cases for Part 1
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

# Test cases for Part 2
test_program4 = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,\
27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
assert feedback_loop(test_program4, [9,8,7,6,5]) == 139629729
assert day07part2(test_program4) == 139629729

test_program5 = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54, \
-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4, \
53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
assert feedback_loop(test_program5, [9,7,8,5,6]) == 18216
assert day07part2(test_program5) == 18216

# Part 1
print("What is the highest signal that can be sent to the thrusters?")
print(day07part1(data)) # Correct answer is 359142

# Part 2
print("In feedback loop mode, what is the highest signal that can be sent to the thrusters?")
print(day07part2(data)) # Correct answer is 4374895
