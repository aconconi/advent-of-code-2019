# Advent of Code 2019
# Day 18: Many-Worlds Interpretation

import networkx as nx
from itertools import combinations
from collections import deque



data_file = "data/day18_test1.dat"
    


lines = open(data_file, "r").read().splitlines()
cols = len(lines[0])
rows = len(lines)
grid = nx.grid_2d_graph(cols, rows)
start = (None, None)
keys = {}
doors = {}
y = 0

for line in lines:
    for x, c in enumerate(line):
        if c == '#':
            grid.remove_node((x,y))
        elif c == '@':
            start = (x, y)
            keys[c] = (x, y)
        elif ord(c) in range(ord('a'), ord('z') ):
            keys[c] = (x, y)
        elif ord(c) in range(ord('A'), ord('Z') ):
            doors[c.lower()] = (x, y)
            # grid.remove_node((x,y))
    y += 1



# pre-compute shortest path len between all pairs of keys
dist = {}
path = {}
doorsinbetween = {}
for k1, k2 in combinations(keys, 2):    
    path[(k1, k2)] = nx.shortest_path(grid, source=keys[k1], target=keys[k2])
    dist[(k1,k2)] = len(path[(k1, k2)])
    doorsinbetween[(k1,k2)] = [z for z in  path[(k1, k2)] if z in doors.keys()]
    
    # replicate entries for inverted keys
    path[(k2, k1)] = path[(k1, k2)]                   
    dist[(k2,k1)] = dist[(k1,k2)]
    doorsinbetween[(k2, k1)] = doorsinbetween[(k1, k2)]

print(path['b', 'd'])
print(doorsinbetween['b', 'd'])
exit(0)

tree = {}    
for k in keys:
    tree[k] = nx.bfs_tree(grid, keys[k], reverse=False, depth_limit=None)

print(tree['@'].nodes())
exit(0)

# seen_can_reach = {}
# def can_reach(k1, k2, havekeys):
#     # print(f"can reach {k1}, {k2}? ", end='')
    
#     hks = ''.join(sorted(havekeys))
#     if (k1, k2, hks) in seen_can_reach:
#         return seen_reachable_keys[(k1, k2, hks)]
    
#     temp = grid.copy()
#     for d in doors:
#         if d not in havekeys:
#             # print(f"Marking door {d}")q
#             temp.remove_node(doors[d])
#     # print(f"temp.nodes = {temp.nodes()}")
#     ans = nx.has_path(temp, source=keys[k1], target=keys[k2])
#     # print(ans)
#     seen_reachable_keys[(k1, k2, hks)] = ans
#     return ans

seen_reachable_keys = {}
# def reachable_keys(grid, source, havekeys):
#     assert source in havekeys
#     temp = grid.copy()
#     for door in (d for d in doors if d not in havekeys):
#         temp.remove_node(doors[door]) 
#     t = nx.bfs_tree(temp, keys[source], reverse=False, depth_limit=None)
#     ans = {p for p in keys if p not in havekeys and keys[p] in t}
    
#     seen_reachable_keys[(source, hks)] = ans
#     return ans 

def reachable_keys(grid, source, havekeys):
    assert source in havekeys
    t = nx.bfs_tree(grid, keys[source], reverse=False, depth_limit=None)
    ans = {p for p in keys if p not in havekeys and keys[p] in t}
    
    seen_reachable_keys[(source, hks)] = ans
    return ans 


seen = {}
def solve(grid, v, havekeys):
    hks = ''.join(sorted(havekeys))
    if (v, hks) in seen:
        return seen[(v, hks)]
    elif len(havekeys)+1 == len(keys):
        # print(f"havekeys {havekeys}")
        return 0
    else:
        havekeys.append(v)
        reach = reachablekeys(grid, v, havekeys)
        cost = float("inf")
        if reach:
            # print(f"reach {reach}")
            cost = min(dist[v,k] + solve(grid, k, havekeys) for k in reach)
        havekeys.pop()
    
    seen[(v, hks)] = cost
    return cost

print(solve(grid, '@', []))