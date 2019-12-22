# Advent of Code 2019
# Day 20: Donut Maze


from itertools import combinations
from collections import deque
import networkx as nx

INF = float("inf")

data_file = "data/day20.dat"
lines = open(data_file, "r").read().splitlines()
width = len(lines[0])
height = len(lines)
graph = nx.grid_2d_graph(width, height)
portals = {}
outers = set()
inners = set()
start = None
finish = None

def is_outer(pos):
    global width, height
    x, y = pos
    return True if x in (2, width - 3) or y in (2, height - 3) else False

def add_portal(label, pos):
    global start, finish, graph, portals
    if label == "AA":
        start = pos
    elif label == "ZZ":
        finish = pos
    else:
        if label in portals:
            graph.add_edge(pos, portals[label], portal=True)
        else:
            portals[label] = pos
        if is_outer(pos):
            outers.add(pos)
        else:
            inners.add(pos)


# Parse grid
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c != '.':
            # keep only walkable nodes
            graph.remove_node((x,y))
        else:
            if line[x + 1].isupper():
                # portal label on the right
                add_portal(line[x+1:x+3], (x, y))
            elif line[x - 1].isupper():
                # portal label on the left
                add_portal(line[x-2:x], (x, y))
            elif lines[y + 1][x].isupper():
                # portal label below
                add_portal(lines[y + 1][x] + lines[y + 2][x], (x, y))
            elif lines[y - 1][x].isupper():
                # portal label above
                add_portal(lines[y - 2][x] + lines[y - 1][x], (x, y))
                                        

def day20part1():
    return nx.shortest_path_length(graph, start, finish)


def day20part2():
    global start, finish, graph, portals, width, height

    # (level, pos, steps)
    todo = deque([(0, start, 0)])
    visited = set([(0, start)])

    while todo:
        level, pos, steps = todo.popleft()
        
        if level == 0 and pos == finish:
            # solution found
            return steps

        for v,_ in graph[pos].items():
            if v in (inners | outers):
                if pos in outers:
                    if level == 0:
                        continue
                    level -= 1
                elif pos in inners:
                    level += 1

            if (level, v) not in visited:
                todo.append((level, v, steps+1))
                visited.add((level, v))
                
                
# Part 1
print("How many steps does it take to get from the open tile marked AA to the open tile marked ZZ?")
print(day20part1()) # 482

# Part 2
print("How many steps does it take to get from the open tile marked AA to the open tile marked ZZ, both at the outermost layer?")
print(day20part2())
