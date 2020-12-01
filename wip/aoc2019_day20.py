# Advent of Code 2019
# Day 20: Donut Maze


from itertools import combinations
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

INF = float("inf")

data_file = "data/day20p.dat"
lines = open(data_file, "r").read().splitlines()


def is_outer(p):
    x, y = p
    print(x,y)
    return True if y == 2 or y == 34 or x == 2 or x == 32 else False
 
# load grid from file and build a graph
cols = len(lines[0])
rows = len(lines)
grid = nx.grid_2d_graph(cols, rows)
start = (None, None)
finish = (None, None)
bridge = {}
y = 0
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c in {'#', ' '} or 'A' <= c <= 'Z':
            grid.remove_node((x,y))
        else:
            if c == '@':
                start = (x,y)
            if c == '!':
                finish = (x,y)
            if '0' <= c <= '9' or 'a' <= c <= 'z':
                if c in bridge.keys():
                    bridge[c].append((x,y))
                else:
                    bridge[c] = [(x,y)]                      

assert is_outer(start)
assert is_outer(finish)
# print(start)
# print(is_outer(start))
# print(finish)
# print(is_outer(finish))
# print(bridge)
# print(grid.nodes[(13,16)]['name'])


for p in bridge:
    x1, y1 = bridge[p][0]
    x2, y2 = bridge[p][1]
    
    # we want each bridge to go from inner to outer edge
    if is_outer((x1, y1)):
        # x1,y1 is on the outer edge. need to swap
        bridge[p][0] = (x2, y2)
        bridge[p][1] = (x1, y1)
    
    # add edge corresponding to bridge
    grid.add_edge((bridge[p][0]), bridge[p][1])

# Part 1
print("how many steps does it take to get from the open tile marked AA to the open tile marked ZZ?")
print(nx.shortest_path_length(grid, start, finish)) # 482
# length, path = nx.bidirectional_dijkstra(grid, start, finish)

# Part 2
inner = [bridge[p][0] for p in bridge]
outer = [bridge[p][1] for p in bridge] + [start, finish]
print(inner)
for p in outer:
    assert is_outer(p)

# dist = {}
# INF = float("inf")
# for k1, k2 in combinations(bridge.keys(), 2):
#     try:
#         dist[(k1,k2)] = nx.shortest_path_length(grid, bridge[k1][0], bridge[k2][1]) - 1
#     except:
#         dist[(k1,k2)] = INF
            
#     # replicate entries for inverted keys
#     dist[(k2, k1)] = dist[(k1, k2)]

# def reachable(state):
#     x, y, z = state
#     if z == 0:
#         return [v for v in grid.neighbors((x, y))]
#     else:
#         assert z > 0        
#         reach2d = [v for v in grid.neighbors((x, y)) if z == 0 or v not in {start, finish}]
#         return [(z-1 if is_outer((x,y)) else z+1, x, y) for (x, y) in reach2d]
    

# memoized = {}
# def solve(state, path):
#     if state in memoized:
#         if not len(memoized) % 100000:
#             print(f"cached: {len(memoized)}")
#         return memoized[state]
        
#     if state == (finish[0], finish[1], 0):
#         print(f"solution found with state={state} path={path}")
#         return 0
#     else:
#         mincost = INF
#         cost = {}
#         reach = reachable(state)
#         for k in reach:
#             if dist[, k] < mincost:
#                 # print(f"Can reach {reach} from {state} considering {v} with havekeys={havekeys}")
#                 cost[v, k] = dist[v, k] + solve(new_state(state, v, k), list(set(state + havekeys)))
#                 if cost[v, k] < mincost:
#                     mincost = cost[v, k]

#     memoized[m] = mincost
#     return mincost
