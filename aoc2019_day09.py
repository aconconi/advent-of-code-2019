# Advent of Code 2019
# Day 9: Sensor Boost


class IntComputer():
    def __init__(self, program, input_values=[]):
        self.mem = {i: v for i, v in enumerate(program)}
        self.pc = 0
        self.relative_base = 0
        self.input_buffer = input_values
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

        def par(i):
            mode = self.command[3-i]
            par = mem_read(self.pc+i)
            if mode == '0':
                # Position mode
                return mem_read(par)
            elif mode == '1':
                # Immediate mode
                return par
            elif mode == '2':
                # Relative mode
                return mem_read(self.relative_base + par)
            else:
                raise Exception("Unknown read mode: {mode}")

        def w_par(i):
            mode = self.command[3-i]
            par = mem_read(self.pc+i)
            if mode == '0':
                # Position mode
                return par
            elif mode == '1':
                # Immediate mode
                raise Exception("Invalid write mode: {mode}")
            elif mode == '2':
                # Relative mode
                return self.relative_base + par
            else:
                raise Exception("Unknown write mode: {mode}")

        def mem_read(loc):
            if loc < 0:
                raise Exception("Invalid memory read from location:", loc)
            return self.mem[loc] if loc in self.mem else 0

        def mem_write(loc, val):
            if loc < 0:
                raise Exception("Invalid memory write to location:", loc)
            self.mem[loc] = val

        i = 0
        while self.mem[self.pc] != 99:
            # pad string with 0 so that it's always 5 digits
            self.command = str(self.mem[self.pc]).zfill(5)
            opcode = int(self.command[3:])   # opcode is two rightmost digits
            i += 1
            # print("step", i, "command", self.command[3:], self.command[2], self.command[1], self.command[0])
            if opcode in [1, 2]:
                # Operation: sum or multiply
                a, b, c = par(1), par(2), w_par(3)
                mem_write(c, a + b if opcode == 1 else a * b)
                self.pc += 4
            elif opcode == 3:
                # Operation: input
                a, b = w_par(1), self.input_buffer.pop(0)
                mem_write(a, b)
                self.pc += 2
            elif opcode == 4:
                # Operation: output
                a = par(1)
                self.output_buffer.append(a)
                self.pc += 2
                # if stepping, give back control after output
                # if self.stepping:
            elif opcode == 5:
                # Operation: jump-if-true
                a, b = par(1), par(2)
                self.pc = b if a != 0 else self.pc+3
            elif opcode == 6:
                # Operation: jump-if-false
                a, b = par(1), par(2)
                self.pc = b if a == 0 else self.pc+3
            elif opcode == 7:
                # Operation: less-than
                a, b, c = par(1), par(2), w_par(3)
                mem_write(c, 1 if a < b else 0)
                self.pc += 4
            elif opcode == 8:
                # Operation: equal
                a, b, c = par(1), par(2), w_par(3)
                mem_write(c, 1 if a == b else 0)
                self.pc += 4
            elif opcode == 9:
                # Operation: relative base offset
                a = par(1)
                self.relative_base += a
                self.pc += 2
            else:
                print("Invalid opcode found:", opcode)
                exit(1)

        # program terminated
        return None


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

# Part 1
print("What BOOST keycode does it produce?")
print(day09part1(data)[0])  # Correct answer is 3765554916

# print(day09part1([9,4, 204,0, 99], [1000]))
print("What are the coordinates of the distress signal?")
print(day09part2(data)[0])  # Correct answer is 76642

# # Part 2
# print("In feedback loop mode, what is the highest signal that can be sent to the thrusters?")
# print(day07part2(data)) # Correct answer is
