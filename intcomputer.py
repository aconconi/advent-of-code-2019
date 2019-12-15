# IntComputer for Advent of Code 2019 puzzles

from collections import defaultdict
import unittest


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
    def __init__(self, program, input_buffer, input_function = None):
        self.mem = defaultdict(int)
        self.pc = 0
        self.relative_base = 0
        self.input_function = input_function
        self.input_buffer = input_buffer
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
    
    # Operation functions
    def _op_sum(self): # 1
        self.mem[self.cx] = self.ax + self.bx
        
    def _op_mul(self): # 2
        self.mem[self.cx] = self.ax * self.bx

    def _op_in(self): # 3
        if not self.input_buffer and self.input_function:
            self.input_buffer.append(self.input_function())
        d = self.input_buffer.pop(0)
        if not isinstance(d, int):
            raise Exception(f"Invalid input type:", d)
        self.mem[self.ax] = d
    
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
        if not isinstance(val, int):
            raise Exception(f"Invalid input type: {val}")
        self.input_buffer.append(val)

    def pop_output(self):
        return self.output_buffer.pop(0) if self.output_buffer else None

    # Parameters functions
    def load_registers(self):
        args = [None] * 3
        modes = str(self.mem[self.pc]).zfill(5)[:3]  # pad string with 0 so that it's always 5 digits
        for i, kind in enumerate(self.OPERATIONS[self.opcode][1]):
            if kind not in {READ,WRITE}:
                raise Exception("Unknown kind: {kind}")
            args[i] = self.r_par(i+1, modes) if kind == READ else self.w_par(i+1, modes)
        (self.ax, self.bx, self.cx) = args  
        

    def r_par(self, i, modes):
        mode = modes[3-i]
        par  = self.mem[self.pc + i]
        if mode == POSITION:
            return self.mem[par]
        elif mode == IMMEDIATE:
            return par
        elif mode == RELATIVE:
            return self.mem[self.relative_base + par]
        else:
            raise Exception(f"Unknown read mode: {mode}")

    def w_par(self, i, modes):
        mode = modes[3-i]
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
            
            # if stepping, return after each output
            if self.stepping and self.opcode == OP_OUT and len(self.output_buffer) == self.expected_out:
                return False

        # program terminated
        self.stepping = False
        return True



class TestIntComputer(unittest.TestCase):
    def test_some(self):
        # Test cases from scul repo
        program = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
        IntComputer(program, [7]).run()
        for i in [7, 8, 9]:
            computer = IntComputer(program, [i])
            computer.run()
            self.assertEqual(computer.pop_output(), (i == 8))

        program = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]
        for i in [7, 8, 9]:
            computer = IntComputer(program, [i])
            computer.run()        
            self.assertEqual(computer.pop_output(), (i < 8))

        program = [3, 3, 1108, -1, 8, 3, 4, 3, 99]
        for i in [7, 8, 9]:
            computer = IntComputer(program, [i])
            computer.run()
            self.assertEqual(computer.pop_output(), (i == 8))

        program = [3, 3, 1107, -1, 8, 3, 4, 3, 99]
        for i in [7, 8, 9]:
            computer = IntComputer(program, [i])
            computer.run()
            self.assertEqual(computer.pop_output(), (i < 8))

        for i in [0, 1, -2]:
            program = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
            computer = IntComputer(program, [i])
            computer.run()
            self.assertEqual(computer.pop_output(), (i != 0))
            
            program = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]
            computer = IntComputer(program, [i])
            computer.run()
            self.assertEqual(computer.pop_output(),  (i != 0))

        program = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125,
                20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]
        a = {7: 999, 8: 1000, 9: 1001}
        for i in [7, 8, 9]:
            computer = IntComputer(program, [i])
            computer.run()
            assert computer.pop_output() == a[i]
        
        
    # Test cases from Day 9
    def test_day9_test1(self):
        program = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
        computer = IntComputer(program, [1])
        computer.run()
        self.assertTrue( computer.output_buffer == [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99])

    def test_day9_test2(self):        
        program = [1102,34915192,34915192,7,4,7,99,0]
        computer = IntComputer(program, [1])
        computer.run()
        self.assertTrue( len(str(computer.pop_output())) == 16)
        
    def test_day9_test3(self):   
        program = [104,1125899906842624,99]
        computer = IntComputer(program, [1])
        computer.run()
        self.assertTrue( computer.output_buffer == [1125899906842624] )


if __name__ == '__main__':
    unittest.main()
