from collections import defaultdict

POSITION  = '0'
IMMEDIATE = '1'
RELATIVE  = '2'

OP_ADD = 1
OP_MUL = 2
OP_IN = 3
OP_OUT = 4
OP_JT = 5
OP_JF = 6
OP_LT = 7
OP_EQ = 8
OP_ADJ = 9
OP_HALT = 99

READ = 0
WRITE = 1

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
    def __init__(self, program, input_values):
        self.mem = defaultdict(int)
        for i,v in enumerate(program):
            self.mem[i] = v 
        self.pc = 0
        self.relative_base = 0
        self.input_buffer = input_values
        self.output_buffer = []
        self.command = ""
        self.opcode = 0
        self.ax = self.bx = self.cx = 0   
        self.stepping = False     
        # self.ARITY = {99: 0, 1: 3, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 9: 1}
        self.steps = 0

        self.OPERATIONS = {
            OP_ADD: ( self.op_sum, [READ, READ, WRITE] ), #1
            OP_MUL: ( self.op_mul, [READ, READ, WRITE] ), #2
            OP_IN:  ( self.op_in,  [WRITE] ), #3
            OP_OUT: ( self.op_out, [READ] ), #4
            OP_JT:  ( self.op_jt,  [READ, READ] ), #5
            OP_JF:  ( self.op_jf,  [READ, READ] ), #6
            OP_LT:  ( self.op_lt,  [READ, READ, WRITE] ), #7
            OP_EQ:  ( self.op_eq,  [READ, READ, WRITE] ), #8
            OP_ADJ: ( self.op_adj, [READ] ), #9
            OP_HALT: ( self.op_halt, [] ) #99
        }
        
    def arity(self, opcode):
        (_, args) = self.OPERATIONS[opcode]
        return len(args)
    
    # Memory read/write
    # def mem_read(self, loc):
    #     if loc < 0:
    #         raise Exception("Invalid memory read from location:", loc)
    #     return self.mem[loc] if loc in self.mem else 0

    # def mem_write(self, loc, val):
    #     if loc < 0:
    #         raise Exception("Invalid memory write to location:", loc)
    #     self.mem[loc] = val
        
    # Operation functions
    def op_sum(self): # 1
        self.mem[self.cx] = self.ax + self.bx
        
    def op_mul(self): # 2
        self.mem[self.cx] = self.ax * self.bx

    def op_in(self): # 3
        self.mem[self.ax] = self.input_buffer.pop(0)
    
    def op_out(self): # 4
        self.output_buffer.append(self.ax)
        
    def op_jt(self): # 5
        self.pc = self.bx if self.ax != 0 else self.pc+3

    def op_jf(self): # 6
        self.pc = self.bx if self.ax == 0 else self.pc+3

    def op_lt(self): # 7
        self.mem[self.cx] = 1 if self.ax < self.bx else 0

    def op_eq(self): # 8
        self.mem[self.cx] = 1 if self.ax == self.bx else 0

    def op_adj(self): # 9
        self.relative_base += self.ax
        
    def op_halt(self):
        return True

  
    # I/O functions
    def append_input(self, val):
        self.input_buffer.append(val)

    def pop_output(self):
        return self.output_buffer.pop(0) if self.output_buffer else None

    # Parameters functions
    def load_registers(self):
        if self.opcode in [OP_ADD, OP_MUL, OP_LT, OP_EQ]: #1,2,7,8
            self.ax = self.r_par(1)
            self.bx = self.r_par(2)
            self.cx = self.w_par(3)
        elif self.opcode == OP_IN:
            self.ax = self.w_par(1)
        elif self.opcode == OP_OUT:             
            self.ax = self.r_par(1)
        elif self.opcode in [OP_JT, OP_JF]:
            self.ax = self.r_par(1)
            self.bx = self.r_par(2)
        elif self.opcode == OP_ADJ:
            self.ax = self.r_par(1)
        elif self.opcode == OP_HALT:
            pass
        else:
            raise Exception("Invalid opcode: {opcode}")

    def r_par(self, i):
        # print("in r_par i", i, "self.command", self.command, "[3-1]", self.command[3-i]) 
        mode = self.command[3-i]
        par  = self.mem[self.pc + i]
        if mode == POSITION:
            # Position mode
            return self.mem[par]
        elif mode == IMMEDIATE:
            # Immediate mode
            return par
        elif mode == RELATIVE:
            # Relative mode
            return self.mem[self.relative_base + par]
        else:
            raise Exception("Unknown read mode: {mode}")

    def w_par(self, i):
        mode = self.command[3-i]
        par  = self.mem[self.pc + i]
        if mode == POSITION:
            return par
        elif mode == IMMEDIATE:
            raise Exception("Invalid write mode: {mode}")
        elif mode == RELATIVE:
            return self.relative_base + par
        else:
            raise Exception("Unknown write mode: {mode}")

    # Execution functions
    def step(self):
        self.stepping = True
        return self.run()
   
    def run(self):
        while self.mem[self.pc] != OP_HALT:
            self.steps += 1
            prev_pc = self.pc
            self.command = str(self.mem[self.pc]).zfill(5)  # pad string with 0 so that it's always 5 digits
            self.opcode  = int(self.command[3:])   # opcode is two rightmost digits
            # print("IntComputer step", self.steps, "command", self.command[3:], self.command[2], self.command[1], self.command[0])
            if self.opcode in self.OPERATIONS:
                self.load_registers()
                self.OPERATIONS[self.opcode][0]()
            else:
                raise("Invalid opcode: {opcode}")
            
            if self.pc == prev_pc:
                 # increment pc only if it was not modified by an operation
                self.pc += self.arity(self.opcode) + 1
            
            # if stepping, return after each output.
            if self.stepping and self.opcode == OP_OUT:
                # print("returning after step")
                return False

        # program terminated
        self.stepping = False
        return True
