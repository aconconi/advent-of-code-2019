# Advent of Code 2019
# Day 18: Many-Worlds Interpretation

import networkx as nx
from itertools import combinations
import matplotlib.pyplot as plt

data_file = "data/day18.dat"
    
# load grid from file and build a graph
lines = open(data_file, "r").read().splitlines()
cols = len(lines[0])
rows = len(lines)
grid = nx.grid_2d_graph(cols, rows)
keys = {}
doors = {}
y = 0
for line in lines:
    for x, c in enumerate(line):
        if c == '#':
            grid.remove_node((x,y))
        elif 'a' <= c <= 'z' or c == '@':
            keys[c] = (x, y)
        elif 'A' <= c <= 'Z':
            doors[c.lower()] = (x, y)
    y += 1

# # build a graph only for keys
# graph = nx.Graph()
# for k in keys:
#     graph.add_node(k)
# for d in doors:
#     graph.add_node(k)

inbetween = {}
dist = {}
for k1, k2 in combinations(keys, 2):
    sp = nx.shortest_path(grid, source=keys[k1], target=keys[k2])
    dist[(k1,k2)] = len(sp) - 1
    inbetween[(k1,k2)] = [d for d in doors if d not in {k1, k2} and doors[d] in sp]
    
    # replicate entries for inverted keys
    inbetween[(k2, k1)] = inbetween[(k1, k2)]
    dist[(k2, k1)] = dist[(k1, k2)]
    
    # graph.add_edge(k1, k2, weight=len(sp) - 1)

    
# pos = nx.circular_layout(graph)  # positions for all nodes
# nx.draw_networkx_nodes(graph, pos)
# nx.draw_networkx_edges(graph, pos)
# edge_labels = nx.get_edge_attributes(graph,'weight')
# nx.draw_networkx_edge_labels(graph,pos, edge_labels=edge_labels)
# nx.draw_networkx_labels(graph, pos)
# plt.axis('off')
# plt.show()

# print(inbetween)


def reachable_keys(source, havekeys):
    assert source in havekeys
    targetkeys = [k for k in keys if k not in havekeys]
    return [k for k in targetkeys if set(inbetween[source, k]).issubset(set(havekeys))]

memoized = {}
inf = float("inf")
def solve(v, havekeys):
    hks = ''.join(sorted(havekeys))
    if (v, hks) in memoized:
        # print("cache hit!")
        return memoized[(v, hks)]
    
    # print(f"Visiting {v} with havekeys={havekeys}")
    havekeys.append(v)
    
    if len(havekeys) == len(keys):
        # print(f"solution found with havekeys={havekeys} cost={sum_path(havekeys)}")
        return 0
    else:
        reach = reachable_keys(v, havekeys)
        # print(f"Can reach {reach} from {v} with havekeys={havekeys}")
        cost = inf
        if reach:
            # print(f"reach {reach}")
            cost = min(dist[v, k] + solve(k, havekeys.copy()) for k in reach)

    havekeys.pop()
    memoized[(v, hks)] = cost
    return cost

def sum_path(path):
    return sum([dist[a,b] for a,b in zip(path, path[1:])])

# Part 1
print("How many steps is the shortest path that collects all of the keys?")
print(solve('@', []))

# Part 2
