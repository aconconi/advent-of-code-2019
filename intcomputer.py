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

class IntComputer():
    def __init__(self, program, input_values):
        self.mem = defaultdict(int)
        self.pc = 0
        self.relative_base = 0
        self.input_buffer = input_values
        self.output_buffer = []
        self.opcode = None
        self.ax = self.bx = self.cx = 0   
        self.stepping = False
        for i,v in enumerate(program):
            self.mem[i] = v
            
        self.expected_out = 0 

        self.OPERATIONS = {
            OP_ADD: ( self._op_sum, [READ, READ, WRITE] ), #1
            OP_MUL: ( self._op_mul, [READ, READ, WRITE] ), #2
            OP_IN:  ( self._op_in,  [WRITE]             ), #3
            OP_OUT: ( self._op_out, [READ]              ), #4
            OP_JT:  ( self._op_jt,  [READ, READ]        ), #5
            OP_JF:  ( self._op_jf,  [READ, READ]        ), #6
            OP_LT:  ( self._op_lt,  [READ, READ, WRITE] ), #7
            OP_EQ:  ( self._op_eq,  [READ, READ, WRITE] ), #8
            OP_ADJ: ( self._op_adj, [READ] ), #9
            OP_HALT: ( self._op_halt, [] ) #99
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
    def _op_sum(self): # 1
        self.mem[self.cx] = self.ax + self.bx
        
    def _op_mul(self): # 2
        self.mem[self.cx] = self.ax * self.bx

    def _op_in(self): # 3
        self.mem[self.ax] = self.input_buffer.pop(0)
    
    def _op_out(self): # 4
        self.output_buffer.append(self.ax)
        
    def _op_jt(self): # 5
        self.pc = self.bx if self.ax != 0 else self.pc+3

    def _op_jf(self): # 6
        self.pc = self.bx if self.ax == 0 else self.pc+3

    def _op_lt(self): # 7
        self.mem[self.cx] = 1 if self.ax < self.bx else 0

    def _op_eq(self): # 8
        self.mem[self.cx] = 1 if self.ax == self.bx else 0

    def _op_adj(self): # 9
        self.relative_base += self.ax
        
    def _op_halt(self):
        return True

  
    # I/O functions
    def append_input(self, val):
        self.input_buffer.append(val)

    def pop_output(self):
        return self.output_buffer.pop(0) if self.output_buffer else None

    # Parameters functions
    def load_registers(self):
        args = [None] * 3
        for i, kind in enumerate(self.OPERATIONS[self.opcode][1]):
            if kind not in {READ,WRITE}:
                raise Exception("Unknown kind: {kind}")
            args[i] = self.r_par(i+1) if kind == READ else self.w_par(i+1)
        (self.ax, self.bx, self.cx) = args  
        
        # if self.opcode in [OP_ADD, OP_MUL, OP_LT, OP_EQ]: #1,2,7,8
            # self.ax = self.r_par(1)
            # self.bx = self.r_par(2)
            # self.cx = self.w_par(3)
        # elif self.opcode == OP_IN:
        #     self.ax = self.w_par(1)
        # elif self.opcode == OP_OUT:             
        #     self.ax = self.r_par(1)
        # elif self.opcode in [OP_JT, OP_JF]:
        #     self.ax = self.r_par(1)
        #     self.bx = self.r_par(2)
        # elif self.opcode == OP_ADJ:
        #     self.ax = self.r_par(1)
        # elif self.opcode == OP_HALT:
        #     pass
        # else:
        #     raise Exception("Invalid opcode: {opcode}")

    def r_par(self, i):
        mode = str(self.mem[self.pc]).zfill(5)[3-i]  # pad string with 0 so that it's always 5 digits
        par  = self.mem[self.pc + i]
        if mode == POSITION:
            return self.mem[par]
        elif mode == IMMEDIATE:
            return par
        elif mode == RELATIVE:
            return self.mem[self.relative_base + par]
        else:
            raise Exception(f"Unknown read mode: {mode}")

    def w_par(self, i):
        mode = str(self.mem[self.pc]).zfill(5)[3-i]  # pad string with 0 so that it's always 5 digits
        par  = self.mem[self.pc + i]
        if mode == POSITION:
            return par
        elif mode == IMMEDIATE:
            raise Exception(f"Invalid write mode: {mode}")
        elif mode == RELATIVE:
            return self.relative_base + par
        else:
            raise Exception(f"Unknown write mode: {mode}")

    # Execution functions
    def step(self, expect = 1):
        self.stepping = True
        self.expected_out = expect
        return self.run()
   
    def run(self):
        while self.mem[self.pc] != OP_HALT:
            prev_pc = self.pc
            self.opcode = self.mem[self.pc] % 100
            if self.opcode in self.OPERATIONS:
                self.load_registers()
                self.OPERATIONS[self.opcode][0]()
            else:
                raise Exception(f"Invalid opcode: {self.opcode}")
            
            if self.pc == prev_pc:
                 # increment pc only if it was not modified by an operation
                self.pc += self.arity(self.opcode) + 1
            
            # if stepping, return after each output.
            if self.stepping and self.opcode == OP_OUT and len(self.output_buffer) == self.expected_out:
                # print("returning after step")
                return False

        # program terminated
        self.stepping = False
        return True
