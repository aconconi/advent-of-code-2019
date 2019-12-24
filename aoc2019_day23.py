# Advent of Code 2019
# Day 23: Category Six

from intcomputer_day23 import IntComputer
from collections import deque

# read input file into a list of integers
# expecting just one line of comma separated integers
with open("data/day23.dat", "r") as data_file:
    data = [int(x) for x in data_file.read().split(",")]


WAIT_ADDR = 0
WAIT_X = 1
WAIT_Y = 2

NAT = 255

class Node():
    def __init__(self, index, program, network):
        self.index = index
        self.computer = IntComputer(program, [index], lambda: -1, self.emit)
        self.network = network
        self.state = WAIT_ADDR
        self.packet_addr = None
        self.packet_x = None
        self.packet_y = None
        
    def append_input(self, n):
        self.computer.append_input(n)
   
    def emit(self, n):
        # print(f"emit called on node {self.index} with parameter {n}")
        if self.state == WAIT_ADDR:
            self.packet_addr = n
            self.state = WAIT_X
        elif self.state == WAIT_X:
            self.packet_x = n
            self.state = WAIT_Y
        elif self.state == WAIT_Y:
            self.packet_y = n
            print(f"Sending packet from addr={self.index} to addr={self.packet_addr} x={self.packet_x} y={self.packet_y}")
            self.network[self.packet_addr].append_input(self.packet_x)
            self.network[self.packet_addr].append_input(self.packet_y) 
            self.state = WAIT_ADDR

class Nat():
    def __init__(self, index):
        self.index = index
        self.solution = None
    
    def append_input(self, n):
        self.solution = n

def day23part1(data):
    nodes = {}
    nodes[NAT] = Nat(NAT)
    
    for i in range(50):
        nodes[i] = Node(i, data, nodes)

    tick = 0
    while True:
        tick += 1
        # print(f"Tick {tick}")
        for i in range(50):
            # print(f"Stepping node {i}")
            nodes[i].computer.step()  
            if nodes[NAT].solution:
                 return nodes[NAT].solution
            

# Part 1 
print(day23part1(data)) # Correct answer is 26464