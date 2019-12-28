# Advent of Code 2019
# Day 23: Category Six

from intcomputer_day23 import IntComputer

# read input file into a list of integers
# expecting just one line of comma separated integers
with open("data/day23.dat", "r") as data_file:
    data = [int(x) for x in data_file.read().split(",")]


WAIT_ADDR = 0
WAIT_X = 1
WAIT_Y = 2

NAT = 255

req = 0


def fixed_input():
    global req
    req += 1
    return -1


class Node():
    def __init__(self, index, program, network):
        self.index = index
        self.computer = IntComputer(
            program, [index], lambda: self.request_input(), self.emit)
        self.network = network
        self.state = WAIT_ADDR
        self.packet_addr = None
        self.packet_x = None
        self.packet_y = None
        self.requesting = False

    def request_input(self):
        self.requesting = True
        return -1

    def step(self):
        self.computer.step()

    def append_input(self, n):
        # print(f"Node addr={self.index} receiving appended input {n}")
        self.computer.append_input(n)
        self.requesting = False

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
            # print(f"Node addr={self.index} sending packet to addr={self.packet_addr} x={self.packet_x} y={self.packet_y}")
            self.network[self.packet_addr].append_input(self.packet_x)
            self.network[self.packet_addr].append_input(self.packet_y)
            self.state = WAIT_ADDR


class Nat(Node):
    def __init__(self, index, nodes):
        self.index = index
        self.x = None
        self.y = None
        self.state = WAIT_X
        self.nodes = nodes
        self.solution = set()

    def append_input(self, n):
        # print(f"NAT addr={self.index} receiving appended input {n}")

        if self.state == WAIT_X:
            self.x = n
            self.y = None
            self.state = WAIT_Y
        else:
            self.y = n
            self.state == WAIT_X

    def step(self):
        if all(self.nodes[i].requesting for i in range(50)):
            # network is idle
            if self.x and self.y:
                if self.y in self.solution:
                    return self.y
                else:
                    self.solution.add(self.y)
                    self.nodes[0].append_input(self.x)
                    self.nodes[0].append_input(self.y)

        return None


def day23part1(data):
    nodes = {}
    nat = Nat(NAT, nodes)
    nodes[NAT] = nat

    for i in range(50):
        nodes[i] = Node(i, data, nodes)

    while True:
        for i in range(50):
            nodes[i].step()
            if nodes[NAT].y:
                return nodes[NAT].y


def day23part2(data):
    nodes = {}
    nat = Nat(NAT, nodes)
    nodes[NAT] = nat

    for i in range(50):
        nodes[i] = Node(i, data, nodes)

    while True:
        for i in range(50):
            nodes[i].step()
        solution = nat.step()
        if solution:
            return solution


# Part 1
print("What is the Y value of the first packet sent to address 255?")
print(day23part1(data))  # Correct answer is 26464

# Part 2
print("What is the first Y value delivered by the NAT to the computer at address 0 twice in a row?")
print(day23part2(data))  # Correct answer is 19544
