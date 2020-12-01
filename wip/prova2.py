POSITION = '0'
IMMEDIATE = '1'
RELATIVE = '2'

OP_SUM = 1
OP_MUL = 2
OP_IN = 3
OP_OUT = 4
OP_JT = 5
OP_JF = 6
OP_LT = 7
OP_EQ = 8
OP_ADJ = 9
OP_HALT = 99

READ = 1000
WRITE = 2000

# OPS = {
#     ADD: (READ, READ, WRITE),
#     MUL: (READ, READ, WRITE),
#     IN: (WRITE,),
#     OUT: (READ,),
#     JUMP_TRUE: (READ, READ),
#     JUMP_FALSE: (READ, READ),
#     LESS_THAN: (READ, READ, WRITE),
#     EQUALS: (READ, READ, WRITE),
#     ADD_RELATIVE_BASE: (READ,),
#     HALT: (),
# }


class IntComputer():
    def __init__(self, program, input_values=[]):
        self.mem = {i: v for i, v in enumerate(program)}
        self.pc = 0
        self.relative_base = 0
        self.input_buffer = input_values
        self.output_buffer = []
        self.command = ""
        self.opcode = 0
        self.ax = self.bx = self.cx = 0
        # self.arity = {99: 0, 1: 3, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 9: 1}
        self.OPERATIONS = {
            OP_SUM: (IntComputer.op_sum, [READ, READ, WRITE]),
            OP_MUL: (IntComputer.op_mul, [READ, READ, WRITE]),
            OP_IN:  (IntComputer.op_in,  [WRITE]),
            OP_OUT: (IntComputer.op_out, [READ]),
            OP_JT:  (IntComputer.op_jt,  [READ, READ]),
            OP_JF:  (IntComputer.op_jf,  [READ, READ]),
            OP_LT:  (IntComputer.op_lt,  [READ, READ, WRITE]),
            OP_EQ:  (IntComputer.op_eq,  [READ, READ, WRITE]),
            OP_ADJ: (IntComputer.op_adj, [READ]),
            OP_HALT: (IntComputer.op_halt, [])
        }

    def arity(self, opcode):
        if opcode in self.OPERATIONS:
            return len(self.OPERATIONS[opcode][1])
        else:
            raise Exception("Invalid opcode: {opcode}", opcode)

    # Memory read/write
    def mem_read(self, loc):
        if loc < 0:
            raise Exception("Invalid memory read from location:", loc)
        return self.mem[loc] if loc in self.mem else 0

    def mem_write(self, loc, val):
        if loc < 0:
            raise Exception("Invalid memory write to location:", loc)
        self.mem[loc] = val

    # Operation functions
    def op_sum(self):
        self.mem_write(self.cx, self.ax + self.bx)

    def op_mul(self):
        self.mem_write(self.cx, self.ax * self.bx)

    def op_in(self):
        self.mem_write(self.ax, self.input_buffer.pop(0))

    def op_out(self):
        self.output_buffer.append(self.ax)

    def op_jt(self):
        self.pc = self.bx if self.ax != 0 else self.pc+3

    def op_jf(self):
        self.pc = self.bx if self.ax == 0 else self.pc+3

    def op_lt(self):
        self.mem_write(self.cx, 1 if self.ax < self.bx else 0)

    def op_eq(self):
        self.mem_write(self.cx, 1 if self.ax == self.bx else 0)

    def op_adj(self):
        self.relative_base += self.ax

    def op_halt(self):
        pass

    def r_par(self, x, mode):
        if mode == POSITION:
            return self.mem_read(x)
        elif mode == IMMEDIATE:
            return par
        elif mode == RELATIVE:
            # Relative mode
            return self.mem_read(self.relative_base + x)
        else:
            raise Exception(f"Unknown read mode: {mode}")

    def w_par(self, x, mode):
        if mode == POSITION:
            return x
        elif mode == IMMEDIATE:
            raise Exception(f"Invalid write mode: {mode}")
        elif mode == RELATIVE:
            return self.relative_base + x
        else:
            raise Exception(f"Unknown write mode: {mode}")

    def get_modes(self, opcode):
        return [m for m in reversed(str(opcode).zfill(5)[:3])]

    def get_types(self, opcode):
        return self.OPERATIONS[opcode % 100][1]

    def load_registers(self, opcode):
        modes = self.get_modes(opcode)
        types = self.get_modes(opcode)
        args = [self.mem_read(self.pc + 1 + i) for i in range(3)]

        self.ax = r_par(if types[0] == READ
computer=IntComputer([0])
computer.load_registers(11205)
